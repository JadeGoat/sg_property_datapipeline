import ast
import pandas as pd
from bs4 import BeautifulSoup

def preprocess_mrt_station_info_data(data):
    print("Processing mrt station info...")
    process_data = data.copy()
    process_data = process_data.rename(columns={'name': 'kml_name'})

    # Extract metadata from description
    col_name = ["STATION_NA", "EXIT_CODE"]
    col_name_lower = [col.lower() for col in col_name]
    process_data[col_name_lower] = process_data.apply(
                                        lambda row: pd.Series(extract_table_metadata(row['description'], col_name)),
                                        axis=1
                                   )
    
    # Split coordinates
    process_data[['lat', 'lon']] = process_data.apply(
                                        lambda row: pd.Series((extract_lat_lon(row['coordinates']))),
                                        axis=1
                                   )

    # Final cleanup on columns
    process_data.drop(columns=['coordinates', 'description', 'properties'], inplace=True)
    process_data = process_data.rename(columns={'station_na': 'station_name'})
    return process_data

def preprocess_child_care_info_data(data):
    print("Processing child care info...")
    process_data = data.copy()
    process_data = process_data.rename(columns={'name': 'kml_name'})

    # Extract metadata from description
    col_name = ["ADDRESSPOSTALCODE", "ADDRESSSTREETNAME", "NAME"]
    col_name_lower = [col.lower() for col in col_name]
    process_data[col_name_lower] = process_data.apply(
                                        lambda row: pd.Series(extract_table_metadata(row['description'], col_name)),
                                        axis=1
                                   )
    # Padding postal code with 5 digits
    process_data["addresspostalcode"] = process_data["addresspostalcode"].apply(
                                            lambda x: "0" + x if len(x) == 5 else x
                                        )
    
    # Split coordinates
    process_data[['lat', 'lon']] = process_data.apply(
                                        lambda row: pd.Series((extract_lat_lon(row['coordinates']))),
                                        axis=1
                                   )

    # Final cleanup on columns
    process_data.drop(columns=['coordinates', 'description', 'properties'], inplace=True)

    return process_data

def preprocess_elderly_care_info_data(data):
    print("Processing elderly care info...")
    process_data = data.copy()
    process_data = process_data.rename(columns={'name': 'kml_name'})

    # Extract metadata from description
    col_name = ["ADDRESSPOSTALCODE", "ADDRESSSTREETNAME", "NAME"]
    col_name_lower = [col.lower() for col in col_name]
    process_data[col_name_lower] = process_data.apply(
                                        lambda row: pd.Series(extract_table_metadata(row['description'], col_name)),
                                        axis=1
                                   )
    # Padding postal code with 5 digits
    process_data["addresspostalcode"] = process_data["addresspostalcode"].apply(
                                            lambda x: "0" + x if len(x) == 5 else x
                                        )
    
    # Split coordinates
    process_data[['lat', 'lon']] = process_data.apply(
                                        lambda row: pd.Series((extract_lat_lon(row['coordinates']))),
                                        axis=1
                                   )

    # Final cleanup on columns
    process_data.drop(columns=['coordinates', 'description', 'properties'], inplace=True)

    return process_data

def preprocess_disability_services_info_data(data):
    print("Processing disability services info...")
    process_data = data.copy()
    process_data = process_data.rename(columns={'name': 'kml_name'})

    # Extract metadata from description
    col_name = ["ADDRESSPOSTALCODE", "ADDRESSSTREETNAME", "NAME"]
    col_name_lower = [col.lower() for col in col_name]
    process_data[col_name_lower] = process_data.apply(
                                        lambda row: pd.Series(extract_table_metadata(row['description'], col_name)),
                                        axis=1
                                   )
    # Padding postal code with 5 digits
    process_data["addresspostalcode"] = process_data["addresspostalcode"].apply(
                                            lambda x: "0" + x if len(x) == 5 else x
                                        )
    
    # Split coordinates
    process_data[['lat', 'lon']] = process_data.apply(
                                        lambda row: pd.Series((extract_lat_lon(row['coordinates']))),
                                        axis=1
                                   )

    # Final cleanup on columns
    process_data.drop(columns=['coordinates', 'description', 'properties'], inplace=True)

    return process_data

def preprocess_chas_clinic_info_data(data):
    print("Processing chas clinic info...")
    process_data = data.copy()
    process_data = process_data.rename(columns={'name': 'kml_name'})

    # Extract metadata from description
    col_name = ["POSTAL_CD", "STREET_NAME", "HCI_NAME"]
    col_name_lower = [col.lower() for col in col_name]
    process_data[col_name_lower] = process_data.apply(
                                        lambda row: pd.Series(extract_table_metadata(row['description'], col_name)),
                                        axis=1
                                   )
    
    # Split coordinates
    process_data[['lat', 'lon']] = process_data.apply(
                                        lambda row: pd.Series((extract_lat_lon(row['coordinates']))),
                                        axis=1
                                   )

    # Final cleanup on columns
    process_data.drop(columns=['coordinates', 'description', 'properties'], inplace=True)
    process_data = process_data.rename(columns={'postal_cd': 'addresspostalcode',
                                                'street_name': 'addressstreetname',
                                                'hci_name': 'name'})

    return process_data

def preprocess_hawker_centre_info_data(data):
    print("Processing hawker centre info...")
    process_data = data.copy()

    # Extract metadata from dictionary 
    col_name = ["ADDRESSPOSTALCODE", "ADDRESSSTREETNAME", "NAME"]
    col_name_lower = [col.lower() for col in col_name]
    process_data[col_name_lower] = process_data.apply(
                                        lambda row: pd.Series(extract_dict_metadata(row['properties'], col_name)),
                                        axis=1
                                   )
    # Padding postal code with 5 digits
    process_data["addresspostalcode"] = process_data["addresspostalcode"].apply(
                                            lambda x: "0" + x if len(x) == 5 else x
                                        )
    
    # Split coordinates
    process_data[['lat', 'lon']] = process_data.apply(
                                        lambda row: pd.Series((extract_lat_lon(row['coordinates']))),
                                        axis=1
                                   )
    
    # Final cleanup on columns
    process_data.drop(columns=['coordinates', 'description', 'properties'], inplace=True)

    return process_data
    
def preprocess_healthier_eateries_info_data(data):
    print("Processing healthier eateries info...")
    process_data = data.copy()
    process_data = process_data.rename(columns={'name': 'kml_name'})

    # Extract metadata from description
    col_name = ["ADDRESSPOSTALCODE", "ADDRESSSTREETNAME", "NAME"]
    col_name_lower = [col.lower() for col in col_name]
    process_data[col_name_lower] = process_data.apply(
                                        lambda row: pd.Series(extract_table_metadata(row['description'], col_name)),
                                        axis=1
                                   )
    # Padding postal code with 5 digits
    process_data["addresspostalcode"] = process_data["addresspostalcode"].apply(
                                            lambda x: "0" + x if len(x) == 5 else x
                                        )
    
    # Split coordinates
    process_data[['lat', 'lon']] = process_data.apply(
                                        lambda row: pd.Series((extract_lat_lon(row['coordinates']))),
                                        axis=1
                                   )

    # Final cleanup on columns
    process_data.drop(columns=['coordinates', 'description', 'properties'], inplace=True)

    return process_data

def preprocess_supermarkets_info_data(data):
    print("Processing supermarkets info...")
    process_data = data.copy()
    process_data = process_data.rename(columns={'name': 'kml_name'})

    # Extract metadata from description
    col_name = ["POSTCODE", "STR_NAME", "LIC_NAME"]
    col_name_lower = [col.lower() for col in col_name]
    process_data[col_name_lower] = process_data.apply(
                                        lambda row: pd.Series(extract_table_metadata(row['description'], col_name)),
                                        axis=1
                                   )
    # Padding postal code with 5 digits
    process_data["postcode"] = process_data["postcode"].apply(
                                    lambda x: "0" + x if len(x) == 5 else x
                                )
    
    # Split coordinates
    process_data[['lat', 'lon']] = process_data.apply(
                                        lambda row: pd.Series((extract_lat_lon(row['coordinates']))),
                                        axis=1
                                   )

    # Final cleanup on columns
    process_data.drop(columns=['coordinates', 'description', 'properties'], inplace=True)
    process_data = process_data.rename(columns={'postcode': 'addresspostalcode',
                                                'str_name': 'addressstreetname',
                                                'lic_name': 'name'})

    return process_data

# ====================
# Supporting functions
# ====================
def extract_table_metadata(row, col_list):

    soup = BeautifulSoup(row, 'html.parser')
    results = []
    for col in col_list:
        hci_row = soup.find('th', string=col)
        hci_value = hci_row.find_next_sibling('td').text.strip()
        results.append(hci_value)

    return tuple(results)

def extract_dict_metadata(row, col_list):

    # Need to replace else cannot convert to dict
    temp_row = row.replace("null,", "'',") 
    temp_dict = ast.literal_eval(temp_row)
    
    results = []
    for col in col_list:
        if col in temp_dict.keys():
            results.append(temp_dict[col])

    return tuple(results)

def extract_lat_lon(row):

    temp_list = row.split(",")
    if len(temp_list) >= 2:
        lat = temp_list[1].replace("]", "")
        lon = temp_list[0].replace("[", "")
        return float(lat), float(lon)
    
    return None, None 
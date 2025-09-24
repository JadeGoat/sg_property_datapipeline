import pandas as pd
from postal_code_helper import get_postal_from_address, get_town_from_postal

def preprocess_bus_stop_info_using_api(data, token):
    # Note: Currently, most accurate method of obtain lat, lot, postal code (town)
    print("Processing bus stop info using api...")
    process_data = data.copy()

    # Prepare mask for selected rows
    # Note: Written this way so that the function order can be swap easily by modifying mask
    #mask = process_data['town'].isnull()
    mask = pd.Series([True] * len(process_data))

    # Get postal code for selected rows
    new_values = process_data.loc[mask].apply(
        lambda row: pd.Series(get_postal_from_address(row['RoadName'], token)),
        axis=1
    )
    process_data.loc[mask, 'postal_code'] = new_values.iloc[:, 0].values
    process_data.loc[mask, 'lat'] = new_values.iloc[:, 1].values
    process_data.loc[mask, 'lon'] = new_values.iloc[:, 2].values
    #print(process_data[['postal_code', 'lat', 'lon']].head(10))

    return process_data

def preprocess_bus_stop_info_postal_into_town(data):
    print("Processing bus stop info's postal into town...")
    process_data = data.copy()

    # Prepare mask for selected rows
    # Note: Written this way so that the function order can be swap easily by modifying mask
    #mask = process_data['town'].isnull()
    mask = pd.Series([True] * len(process_data))

    # Get town for selected rows
    new_values = process_data.loc[mask].apply(
        lambda row: pd.Series(get_town_from_postal(row['postal_code'])),
        axis=1
    )

    process_data.loc[mask, 'town'] = new_values.iloc[:, 0].values
    #print(process_data[['postal_code', 'Latitude', 'Longitude', 'town']].head(10))

    return process_data
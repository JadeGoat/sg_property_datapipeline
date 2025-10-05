import pandas as pd
from lxml import etree

def preprocess_mrt_station_info_data(data):
    print("Processing mrt station info...")

    # Prepare dataframe, kml content, xml parser
    process_data = pd.DataFrame(columns=['KmlName', 'StationName', 'ExitCode', 
                                         'IncCrc', 'FmelUpdUD', 'Latitude', 'Longitude'])
    kml_content = data.loc[0, "kml_content"]
    tree = etree.fromstring(kml_content.encode("utf-8"))

    # Search for a the Placemark tag
    placemarks = tree.findall(".//{http://www.opengis.net/kml/2.2}Placemark")
    for pm in placemarks:

        # Initialize variables
        kml_name, lat_lon, station_name = "", "", ""
        exit_code, inc_crc, fmel_upd_d = "", "", ""

        # Extract value and load into variables
        name_obj = pm.find("{http://www.opengis.net/kml/2.2}name")
        coords_obj = pm.find(".//{http://www.opengis.net/kml/2.2}coordinates")
        data_list = pm.findall(".//{http://www.opengis.net/kml/2.2}SimpleData")
        
        kml_name = name_obj.text
        lat_lon = coords_obj.text.split(',')

        for data_obj in data_list:
            data_name = data_obj.get('name').lower()
            if data_name == "station_na":
                station_name = data_obj.text
            elif data_name == "exit_code":
                exit_code = data_obj.text
            elif data_name == "inc_crc":
                inc_crc = data_obj.text
            elif data_name == "fmel_upd_d":
                fmel_upd_d = data_obj.text
       
        # Prepare data into row form
        new_row = {'KmlName': kml_name, 
                   'StationName': station_name, 'ExitCode': exit_code,
                   'IncCrc': inc_crc, 'FmelUpdUD': fmel_upd_d, 
                   'Latitude': lat_lon[1], 'Longitude': lat_lon[0]}
        
        # Add new row to dataframe
        process_data = pd.concat([process_data, pd.DataFrame([new_row])], ignore_index=True)
        
    return process_data
import pandas as pd
from pyproj import Transformer
from postal_code_helper import get_postal_from_svy21, get_town_from_postal, map_to_town

def preprocess_carpark_info_using_api(data, token):
    # Note: Currently, most accurate method of obtain lat, lot, postal code (town)
    print("Processing carpark info using api...")
    process_data = data.copy()

    # Prepare mask for selected rows
    # Note: Written this way so that the function order can be swap easily by modifying mask
    #mask = process_data['town'].isnull()
    mask = pd.Series([True] * len(process_data))

    # Get postal code for selected rows
    new_values = process_data.loc[mask].apply(
        lambda row: pd.Series(get_postal_from_svy21(row['x_coord'], row['y_coord'], token)),
        axis=1
    )
    process_data.loc[mask, 'postal_code'] = new_values.iloc[:, 0].values
    process_data.loc[mask, 'lat'] = new_values.iloc[:, 1].values
    process_data.loc[mask, 'lon'] = new_values.iloc[:, 2].values
    #print(process_data[['postal_code', 'lat', 'lon']].head(10))

    return process_data

def preprocess_carpark_info_postal_into_town(data):
    print("Processing carpark info's postal to town...")
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
    #print(process_data[['postal_code', 'lat', 'lon', 'town']].head(10))

    return process_data

def preprocess_carpark_info_data_using_regex(data):
    print("Processing carpark info using regex...")
    process_data = data.copy()

    # Prepare mask for selected rows
    # Note: Written this way so that the function order can be swap easily by modifying mask
    mask = process_data['postal_code']=="Unknown"

    # Clean up the very dirty 'address' column
    process_data.loc[mask, 'address'] = process_data.loc[mask, 'address'].str.replace(r'\s*[/,&-]\s+', '/', regex=True)
    process_data.loc[mask, 'address'] = process_data.loc[mask, 'address'].str.replace(' TO ','-')
    process_data.loc[mask, 'address'] = process_data.loc[mask, 'address'].str.replace('A-B','A/B')
    process_data.loc[mask, 'address'] = process_data.loc[mask, 'address'].str.replace('BLKS','BLK')
    process_data.loc[mask, 'address'] = process_data.loc[mask, 'address'].str.replace(' BETWEEN ','')
    process_data.loc[mask, 'address'] = process_data.loc[mask, 'address'].str.replace(' AND ',',')
    process_data.loc[mask, 'address'] = process_data.loc[mask, 'address'].str.replace('BED0K','BEDOK')
    
    # ------------------
    # Regex explaination
    # ------------------
    # (?:\d+[A-Za-z]?)
    # Example: 25, 25A
    # (?:[/,\-]\s*(?:\d+[A-Za-z]?|[A-Za-z]))*
    # - [/,\-]\s*: combination of either slash,comma,dash
    # - (?:\d+[A-Za-z]?|[A-Za-z]): number follow by optional alpha or just alpha
    # Part2: eg. 25/26, 25A/26B, 25-30, 25A-26B, 25/26,30, 25A/B/C

    # Split 'address' into' block' and 'town_and_street'
    pattern = r'^(?:(BLK|BLOCK)\s*)?((?:\d+[A-Za-z]?)(?:[/,\-]\s*(?:\d+[A-Za-z]?|[A-Za-z]))*)\s+(.*)'
    new_values = process_data.loc[mask, 'address'].str.extract(pattern)
    process_data.loc[mask, 'prefix'] = new_values.iloc[:, 0].values
    process_data.loc[mask, 'block'] = new_values.iloc[:, 1].values
    process_data.loc[mask, 'town_and_street'] = new_values.iloc[:, 2].values
    #print(process_data[['address', 'block', 'town_and_street']].head(10))

    # ------------------
    # Regex explaination
    # ------------------
    # (STREET|AVENUE)\s+(\d+(?:/\d|)?)
    # Example: STREET 1, STREET 1/2, AVENUE 1, AVENUE 1/2

    # Split into town, street_type, street_number
    pattern = r'^(.*?)(STREET| ST|AVENUE|CENTRAL)\s+(\d+(?:/\d|)?)\b'
    new_values = process_data.loc[mask, 'town_and_street'].str.extract(pattern)
    process_data.loc[mask, 'town'] = new_values.iloc[:, 0].values
    process_data.loc[mask, 'street_type'] = new_values.iloc[:, 1].values
    process_data.loc[mask, 'street_number'] = new_values.iloc[:, 2].values
    #print(process_data[['address', 'town_and_street', 'town']].head(10))

    # Final cleanup on 'town' column
    #process_data.loc[mask, 'town'] = process_data.loc[mask, 'town'].str.replace(r'\s*(ROAD|RD|/)\s*', '', regex=True)
    #process_data.loc[mask, 'town'] = process_data.loc[mask].str.strip()
    new_values = process_data.loc[mask].apply(
        lambda row: pd.Series(map_to_town(row['town'])),
        axis=1
    )
    process_data.loc[mask, 'town'] = new_values.iloc[:, 0].values

    return process_data

def preprocess_carpark_info_address_into_town(data):
    # Note: Best effort to convert address to town. Some erroneous conversion were spotted. 
    #       eg. upper serangoon rd should be under hougang town
    print("Processing carpark info's address into town...")
    process_data = data.copy()

    # Prepare mask for selected rows
    # Note: Written this way so that the function order can be swap easily by modifying mask
    mask = process_data['town']=="Unknown"

    # Get town for selected rows
    new_values =  process_data.loc[mask].apply(
        lambda row: pd.Series(map_to_town(row['address'])),
        axis=1
    )
    process_data.loc[mask, 'town'] = new_values.iloc[:, 0].values

    return process_data

def preprocess_carpark_info_data_for_svy21(data):
    print("Processing carpark info x_coord, y_coord to lat, lot...")
    process_data = data.copy()

    # Define the transformer from SVY21 (EPSG:3414) to WGS84 (EPSG:4326)
    transformer = Transformer.from_crs("EPSG:3414", "EPSG:4326", always_xy=True)

    # Prepare mask for selected rows
    # Note: Written this way so that the function order can be swap easily by modifying mask
    mask = process_data['postal_code']=="Unknown"

    new_values = process_data[mask].apply(
        lambda row: pd.Series(transformer.transform(row['x_coord'], row['y_coord'])),
        axis=1
    )
    process_data.loc[mask, 'lon'] = new_values.iloc[:, 0].values
    process_data.loc[mask, 'lat'] = new_values.iloc[:, 1].values

    return process_data
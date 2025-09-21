import os
import pandas as pd
from SVY21 import SVY21
from dotenv import load_dotenv
from mysql_helper import get_db_engine, read_data_from_db, save_data_to_db
from postal_code_helper import get_postal, get_town_from_postal, map_to_town

def preprocess_carpark_info_using_api(data, token):
    print("Processing carpark info using api...")
    process_data = data.copy()

    # Prepare mask for selected rows
    #mask = process_data['town'].isnull()
    mask = pd.Series([True] * len(process_data))

    # Get postal code for selected rows
    new_values = process_data.loc[mask].apply(
        lambda row: pd.Series(get_postal(row['x_coord'], row['y_coord'], token)),
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

def preprocess_carpark_info_street_into_town(data):
    print("Processing carpark info's street into town...")
    process_data = data.copy()
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
    # Note: The lat lon conversion is not accurate after testing
    # Initialize SVY21 class
    cv = SVY21()
    
    process_data = data.copy()
    mask = process_data['postal_code']=="Unknown"

    new_values = process_data[mask].apply(
        lambda row: pd.Series(cv.computeLatLon(row['x_coord'], row['y_coord'])),
        axis=1
    )
    process_data.loc[mask, 'lat'] = new_values.iloc[:, 0].values
    process_data.loc[mask, 'lon'] = new_values.iloc[:, 1].values

    return process_data

def preprocess_hdb_rental_data(data):
    process_data = data.copy()

    # Split 'month' column and convert to integer
    columns_name = ['approval_year', 'approval_month']
    process_data[columns_name] = process_data['rent_approval_date'].str.split('-', expand=True)
    process_data['approval_year'] = pd.to_numeric(process_data['approval_year'], errors='coerce')
    process_data['approval_month'] = pd.to_numeric(process_data['approval_month'], errors='coerce')

    # Drop unnecessary columns
    process_data.drop(columns='rent_approval_date', inplace=True)

    return process_data

def preprocess_hdb_resale_data(data):
    process_data = data.copy()

    # Split 'month' column and convert to integer
    columns_name = ['transact_year', 'transact_month']
    process_data[columns_name] = process_data['month'].str.split('-', expand=True)
    process_data['transact_year'] = pd.to_numeric(process_data['transact_year'], errors='coerce')
    process_data['transact_month'] = pd.to_numeric(process_data['transact_month'], errors='coerce')
    
    # Split 'remaining_lease' column and convert to integer
    columns_name = ['lease_year', 'lease_month']
    process_data[columns_name] = process_data['remaining_lease'].str.split('years', expand=True)
    process_data['lease_month'] = process_data['lease_month'].str.replace(r'\bmonths?\b', '', regex=True)
    process_data['lease_month'] = pd.to_numeric(process_data['lease_month'], errors='coerce')
    process_data['lease_year'] = pd.to_numeric(process_data['lease_year'], errors='coerce')
    
    # Final cleanup on data type
    process_data = process_data.fillna(0)
    process_data['lease_month'] = process_data['transact_year'].astype(int)
    process_data['lease_month'] = process_data['transact_month'].astype(int)
    process_data['lease_month'] = process_data['lease_year'].astype(int)
    process_data['lease_month'] = process_data['lease_month'].astype(int)

    # Drop unnecessary columns
    process_data.drop(columns='month', inplace=True)
    process_data.drop(columns='remaining_lease', inplace=True)

    return process_data

def average_hdb_rental_data_by_year(data):
    process_data = data.copy()

    # Grouped resale price by year and town
    grouped_columns = ['approval_year', 'town']
    agg_methods = {'monthly_rent': ['mean', 'median']}
    final_data = process_data.groupby(grouped_columns).agg(agg_methods)

    # Final cleanup on grouped data
    final_data = final_data.round(2)
    final_data.columns = ['_'.join(col).strip() 
                          if isinstance(col, tuple) else col 
                          for col in final_data.columns]
    final_data = final_data.reset_index()

    return final_data

def average_hdb_resale_data_by_year(data):
    process_data = data.copy()

    # Feature engineered new resale price
    process_data['resale_per_sqm'] = process_data['resale_price'] / process_data['floor_area_sqm']
    process_data['lease_remaining'] = (process_data['lease_year'] + (process_data['lease_month'] / 12 ))
    process_data['resale_per_lease'] = process_data['resale_price'] / process_data['lease_remaining']
    process_data['resale_per_sqm_per_lease'] = process_data['resale_per_sqm'] / process_data['lease_remaining'] * 100

    # Grouped resale price by year and town
    grouped_columns = ['transact_year', 'town']
    agg_methods = {'resale_price': ['mean', 'median'], 
                   'resale_per_sqm': ['mean', 'median'],
                   'resale_per_lease': ['mean', 'median'],
                   'resale_per_sqm_per_lease': ['mean', 'median']}
    final_data = process_data.groupby(grouped_columns).agg(agg_methods)

    # Final cleanup on grouped data
    final_data = final_data.round(2)
    final_data.columns = ['_'.join(col).strip() 
                          if isinstance(col, tuple) else col 
                          for col in final_data.columns]
    final_data = final_data.reset_index()

    return final_data

def average_hdb_rental_data_by_town(data):
    process_data = data.copy()

    # Grouped resale price by year and town
    grouped_columns = ['approval_year', 'town', 'flat_type']
    agg_methods = {'monthly_rent': ['mean', 'median']}
    final_data = process_data.groupby(grouped_columns).agg(agg_methods)

    # Final cleanup on grouped data
    final_data = final_data.round(2)
    final_data.columns = ['_'.join(col).strip() 
                          if isinstance(col, tuple) else col 
                          for col in final_data.columns]
    final_data = final_data.reset_index()

    return final_data

def average_hdb_resale_data_by_town(data):
    process_data = data.copy()

    # Feature engineered new resale price
    process_data['resale_per_sqm'] = process_data['resale_price'] / process_data['floor_area_sqm']
    process_data['lease_remaining'] = (process_data['lease_year'] + (process_data['lease_month'] / 12 ))
    process_data['resale_per_lease'] = process_data['resale_price'] / process_data['lease_remaining']
    process_data['resale_per_sqm_per_lease'] = process_data['resale_per_sqm'] / process_data['lease_remaining'] * 100

    # Grouped resale price by year and town
    grouped_columns = ['transact_year', 'town', 'flat_type']
    agg_methods = {'resale_price': ['mean'], 
                   'resale_per_sqm': ['mean'],
                   'resale_per_lease': ['mean'],
                   'resale_per_sqm_per_lease': ['mean'],
                   'lease_remaining': ['mean']}
    final_data = process_data.groupby(grouped_columns).agg(agg_methods)

    # Final cleanup on grouped data
    final_data = final_data.round(2)
    final_data.columns = ['_'.join(col).strip() 
                          if isinstance(col, tuple) else col 
                          for col in final_data.columns]
    final_data = final_data.reset_index()

    return final_data

def process_carpark_info(db_engine, process_api=True):

    load_dotenv()
    token = os.getenv('ONE_MAP_API_TOKEN')

    # Database table name
    src_table_name = 'carpark_info'
    dst_table_name = 'carpark_info_clean'

    # Skip process using api if disable as it is time comsuming
    if (process_api):
        raw_data = read_data_from_db(db_engine, src_table_name)
        cleaned_data = preprocess_carpark_info_using_api(raw_data, token)
    else:
        cleaned_data = read_data_from_db(db_engine, dst_table_name)
    
    # First cut processing using API
    cleaned_data = preprocess_carpark_info_postal_into_town(cleaned_data)
    save_data_to_db(db_engine, dst_table_name, cleaned_data)

    # Second cut processing using regex
    dst_table_name = 'carpark_info_clean2'
    cleaned_data = preprocess_carpark_info_data_using_regex(cleaned_data)
    cleaned_data = preprocess_carpark_info_street_into_town(cleaned_data)
    cleaned_data = preprocess_carpark_info_data_for_svy21(cleaned_data)

    save_data_to_db(db_engine, dst_table_name, cleaned_data)

def process_hdb_rental_price(db_engine):

    # Database table name
    src_table_name = 'hdb_rental'
    dst_table_name = 'hdb_rental_clean'
    
    raw_data = read_data_from_db(db_engine, src_table_name)
    cleaned_data = preprocess_hdb_rental_data(raw_data)
    save_data_to_db(db_engine, dst_table_name, cleaned_data)

    dst_table_name = 'hdb_rental_avg_year'
    grouped_data = average_hdb_rental_data_by_year(cleaned_data)
    save_data_to_db(db_engine, dst_table_name, grouped_data)

    dst_table_name = 'hdb_rental_avg_town'
    grouped_data = average_hdb_rental_data_by_town(cleaned_data)
    save_data_to_db(db_engine, dst_table_name, grouped_data)

def process_hdb_resale_price(db_engine):

    # Database table name
    src_table_name = 'hdb_resale'
    dst_table_name = 'hdb_resale_clean'
    
    raw_data = read_data_from_db(db_engine, src_table_name)
    cleaned_data = preprocess_hdb_resale_data(raw_data)
    save_data_to_db(db_engine, dst_table_name, cleaned_data)

    dst_table_name = 'hdb_resale_avg_year'
    grouped_data = average_hdb_resale_data_by_year(cleaned_data)
    save_data_to_db(db_engine, dst_table_name, grouped_data)

    dst_table_name = 'hdb_resale_avg_town'
    grouped_data = average_hdb_resale_data_by_town(cleaned_data)
    save_data_to_db(db_engine, dst_table_name, grouped_data)

if __name__ == "__main__":

    # Create SQLAlchemy engine
    db_engine = get_db_engine()

    process_carpark_info(db_engine, False)
    #process_hdb_rental_price(db_engine)
    #process_hdb_resale_price(db_engine)
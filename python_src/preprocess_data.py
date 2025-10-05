import os
import argparse
from dotenv import load_dotenv
from mysql_helper import get_db_engine, read_data_from_db, save_data_to_db

from preprocess_data_hdb import preprocess_hdb_resale_data, average_hdb_resale_data_by_year 
from preprocess_data_hdb import average_hdb_resale_data_by_year, average_hdb_rental_data_by_town
from preprocess_data_hdb import preprocess_hdb_rental_data, average_hdb_rental_data_by_year
from preprocess_data_hdb import average_hdb_rental_data_by_year, average_hdb_resale_data_by_town

from preprocess_data_carpark import preprocess_carpark_info_using_api, preprocess_carpark_info_postal_into_town
from preprocess_data_carpark import preprocess_carpark_info_address_into_town
#from preprocess_data_carpark import preprocess_carpark_info_data_using_regex, 
from preprocess_data_carpark import preprocess_carpark_info_data_for_svy21
from preprocess_data_mrt_station import preprocess_mrt_station_info_data

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
        # Attempt to read from existing clean table, otherwise raw table
        cleaned_data = read_data_from_db(db_engine, dst_table_name)
        if (cleaned_data is None): 
            cleaned_data = read_data_from_db(db_engine, src_table_name)

    # First cut processing
    cleaned_data = preprocess_carpark_info_postal_into_town(cleaned_data) 
    save_data_to_db(db_engine, dst_table_name, cleaned_data)

    # Second cut processing using regex
    dst_table_name = 'carpark_info_clean2'
    #cleaned_data = preprocess_carpark_info_data_using_regex(cleaned_data) # not required now, for future expansion
    cleaned_data = preprocess_carpark_info_address_into_town(cleaned_data) # not reliable, otherwise missing town info
    cleaned_data = preprocess_carpark_info_data_for_svy21(cleaned_data)

    save_data_to_db(db_engine, dst_table_name, cleaned_data)

def process_mrt_station_info(db_engine):
    # Database table name
    src_table_name = 'lta_mrt'
    dst_table_name = 'lta_mrt_clean'

    raw_data = read_data_from_db(db_engine, src_table_name)
    cleaned_data = preprocess_mrt_station_info_data(raw_data)
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

    # Create the parser to process --api arugment
    parser = argparse.ArgumentParser()
    parser.add_argument("--api", type=str, help="flag to enable/disable one map api", default=True)
    args = parser.parse_args()

    # Convert string to boolean
    flag = str(args.api).strip().lower() in ("true")

    # Create SQLAlchemy engine
    db_engine = get_db_engine()

    process_hdb_rental_price(db_engine)
    process_hdb_resale_price(db_engine)
    process_carpark_info(db_engine, flag)
    process_mrt_station_info(db_engine)
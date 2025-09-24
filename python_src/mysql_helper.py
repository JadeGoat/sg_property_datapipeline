import os
import csv
import json
import geojson
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

from dateutil.parser import parse as parse_date

# Retrieve config for mysql-connector-python package
def get_db_config():

    # Load environment variables from .env file
    load_dotenv()

    # MySQL connection details
    db_config = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME')
    }
    return db_config

# Retrieve engine for sqlalchemy package
def get_db_engine():

    # Load environment variables from .env file
    load_dotenv()

    # Get MySQL credentials
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    database = os.getenv('DB_NAME')

    db_engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")
    return db_engine

# ====================================
# CSV to MySQL functions
# - use mysql-connector-python package
# ====================================
def create_table_from_csv(csv_file, cursor, table_name, no_of_samples=1000):

    # Read first 20 rows to determine data type
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        sample_rows = [row for _, row in zip(range(no_of_samples), reader)]  # Sample first 'n' rows
        types = infer_column_types(sample_rows)

    # Create table based on data type
    columns = ', '.join([f"`{name}` {dtype}" for name, dtype in zip(headers, types)])
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    cursor.execute(f"CREATE TABLE {table_name} ({columns})")

def insert_data_from_csv(csv_file, cursor, table_name):

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader) # Skip header

        # Insert data
        for row in reader:
            placeholders = ', '.join(['%s'] * len(row))
            cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", row)

    print(f"CSV data loaded into MySQL table '{table_name}' successfully.")

def infer_type(value):
    try:
        int(value)
        return 'INT'
    except:
        try:
            float(value)
            return 'FLOAT'
        except:
            try:
                parse_date(value)
                return 'VARCHAR(255)'
            except:
                return 'VARCHAR(255)'

def infer_column_types(sample_rows):
    types = []
    for col in zip(*sample_rows):
        inferred = [infer_type(val) for val in col if val.strip() != '']
        if not inferred:
            types.append('VARCHAR(255)')
        elif 'VARCHAR(255)' in inferred:
            types.append('VARCHAR(255)')
        elif 'DATE' in inferred:
            types.append('DATE')
        elif 'FLOAT' in inferred:
            types.append('FLOAT')
        else:
            types.append('INT')
    return types

# ====================================
# GEOJSON to MySQL functions
# - use mysql-connector-python package
# - use geojson package
# ====================================
def create_table_for_geojson(cursor, table_name):

    # Drop table if exists
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    
    # Create table (if not exists)
    columns = """
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                description TEXT,
                coordinates TEXT,
                properties JSON
              """
    cursor.execute(f"CREATE TABLE {table_name} ({columns})")

def insert_data_from_geojson(geojson_file, cursor, table_name):

    # Load GeoJSON file
    with open(geojson_file) as f:
        data = geojson.load(f)

    # Insert each feature
    for feature in data['features']:
        props = feature.get('properties', {})
        name = props.get('Name', 'Unnamed')
        description = props.get('Description', '')
        coords = feature['geometry']['coordinates']
        properties_metadata = feature.get('properties', {})
        properties_metadata_json = json.dumps(properties_metadata)

        # Note: table name is not escaped, while remaining fields are escaped 
        query = f"""
            INSERT INTO `{table_name}` (name, description, coordinates, properties)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (name, description, str(coords), properties_metadata_json))
    
    print(f"GeoJson data loaded into MySQL table '{table_name}' successfully.")

# =========================
# MySQL operation functions
# - use sqlalchemy package
# =========================
def read_data_from_db(engine, table_name):
    
    query = "SELECT * FROM " + table_name
    try:
        data = pd.read_sql(query , con=engine)
        print("Data read from MySQL table '" + table_name + "'")
    except:
        print("Error read operation")
        return None
    
    return data

def save_data_to_db(engine, table_name, data, save_index=False):
    
    try:
        data.to_sql(name=table_name, con=engine, if_exists='replace', index=save_index)
        print("Data written to MySQL table '" + table_name + "'")
    except:
        print("Error write operation")
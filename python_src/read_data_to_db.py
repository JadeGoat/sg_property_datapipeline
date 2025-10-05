import os
import mysql.connector
from mysql_helper import get_db_config
from mysql_helper import create_table_from_csv, insert_data_from_csv
from mysql_helper import create_table_for_geojson, insert_data_from_geojson
from mysql_helper import create_table_for_kml, insert_data_from_kml

def load_csv_into_database(csv_file, db_config, table_name):
   
    # Connect to MySQL
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    create_table_from_csv(csv_file, cursor, table_name)
    insert_data_from_csv(csv_file, cursor, table_name)
    
    # Commit and close
    conn.commit()
    cursor.close()
    conn.close()

def load_geojson_into_database(geojson_file, db_config, table_name):
   
    # Connect to MySQL
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    create_table_for_geojson(cursor, table_name)
    insert_data_from_geojson(geojson_file, cursor, table_name)
    
    # Commit and close
    conn.commit()
    cursor.close()
    conn.close()

def load_kml_into_database(kml_file, db_config, table_name):

     # Connect to MySQL
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    create_table_for_kml(cursor, table_name)
    insert_data_from_kml(kml_file, cursor, table_name)
    
    # Commit and close
    conn.commit()
    cursor.close()
    conn.close()
    
if __name__ == "__main__":

    # Database details
    db_config = get_db_config()
    
    # Tabular storage for csv type
    db_table_name_csv_array = [
        'hdb_rental', 
        'hdb_resale',
        'carpark_info', 
        'bus_stop_info'
    ]
    csv_filename_array = [
        "hdb_rental_data.csv",
        "hdb_resale_data.csv",
        "carpark_data.csv",
        "busstop_data.csv",
    ]

    # Json Storage for geojson type
    db_table_name_geojson_array = [
        'child_care', 
        'elderly_care', 
        'hawker_centre', 
        'healthier_eateries'
    ]
    geojson_filename_array = [
        "child_care_data.geojson",
        "elderly_care_data.geojson",
        "hawker_centre_data.geojson",
        "healthier_eateries_data.geojson",
    ]

    # Longtext storage for kml type
    db_table_name_kml_array = [
        'lta_mrt', 
    ]
    kml_filename_array = [
        "lta_mrt.kml",
    ]

    for filename, db_table_name in zip(csv_filename_array, db_table_name_csv_array):
        
        # Append filename to working directory
        csv_filename = os.path.join(os.getcwd(), '..', 'data', filename)

        print("Loading " + filename + " to database table " + db_table_name + "...")
        load_csv_into_database(csv_filename, db_config, db_table_name)

    for filename, db_table_name in zip(geojson_filename_array, db_table_name_geojson_array):
        
        # Append filename to working directory
        geojson_filename = os.path.join(os.getcwd(), '..', 'data', filename)

        print("Loading " + filename + " to database table " + db_table_name + "...")
        load_geojson_into_database(geojson_filename, db_config, db_table_name)

    for filename, db_table_name in zip(kml_filename_array, db_table_name_kml_array):
        
        # Append filename to working directory
        kml_filename = os.path.join(os.getcwd(), '..', 'data', filename)

        print("Loading " + filename + " to database table " + db_table_name + "...")
        load_kml_into_database(kml_filename, db_config, db_table_name)
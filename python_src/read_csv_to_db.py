import os
import mysql.connector
from mysql_helper import get_db_config, create_table_from_csv, insert_data_from_csv

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
    
if __name__ == "__main__":

    # Database details
    db_config = get_db_config()
    db_table_name = 'hdb_resale'

    # Append filename to working directory
    csv_file = os.path.join(os.getcwd(), '..', 'data', 'ResaleFlatPrices', 'data.csv')

    load_csv_into_database(csv_file, db_config, db_table_name)
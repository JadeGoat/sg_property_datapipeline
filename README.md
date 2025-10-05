# Setup
#### Preparing virtual environment
```
pip install virtualenv
python -m virtualenv sg_property_env
```

#### Installing package into virtual environment
```
.\sg_property_env\Scripts\activate
pip install mysql-connector-python
pip install SQLAlchemy
pip install geojson 
pip install python-dotenv
pip install python-dateutil
pip install pandas
pip install requests
pip install pyproj
```

#### Preparing .env file
Creating .env in python_src folder with the following field
```
DB_HOST = <to_fill_in_database_url>
DB_USER = <to_fill_in_database_username>
DB_PASSWORD = <to_fill_in_database_password>
DB_NAME = <to_fill_in_database_name>
ONE_MAP_API_TOKEN = <register_one_map_api_key_and_fill_in>
```

Optional (Required for get_onemap_token.py script)
```
ONE_MAP_API_EMAIL = <email_that_registered_with_one_map_and_fill_in>
ONE_MAP_API_PASSWORD = <password_used_with_email_with_one_map_and_fill_in>
```

#### Data
Copy the following data from data.gov.sg to the data/ folder or running the download_csv.py

Method 1 

Download from data.gov.sg
1. Resale flat prices based on registration date from Jan-2017 onwards (save as "hdb_resale_data.csv")
2. Renting Out of Flats 2025 (save as "hdb_rental_data.csv")
3. Carpark Availability (save as "carpark_data.csv")
4. Child Care Services (save as "child_care_data.geojson")
5. Eldercare Services (save as "elderly_care_data.geojson")
6. Hawker Centres (save as "hawker_centre_data.geojson")
7. Healthier Eateries (save as "healthier_eateries.geojson")
8. LTAMRTStationExitKML (save as "lta_mrt.kml")

Download from lta datamall.gov.sg
1. Dynamic Dataset, Public Transport, Bus Stops (save as "busstop_data.csv")

Method 2 (Run download_data.py)
```
python ./download_data.py
```

#### Folder Structure
```
├─ data
|  ├─ busstop_data.csv
|  ├─ carpark_data.csv
|  ├─ hdb_rental_data.csv
|  ├─ hdb_resale_data.csv
|  ├─ child_care_data.geojson
|  ├─ elderly_care_data.geojson
|  ├─ hawker_centre_data.geojson
|  └─ healthier_eateries_data.geojson
├─ python_src
|  ├─ .env
|  ├─ download_data.py
|  ├─ get_onemap_token.py
|  ├─ mysql_helper.py
|  ├─ postal_code_helper.py
|  ├─ preprocess_data.py
|  └─ read_data_to_db.py
├─ sg_property_env
├─ .gitignore
└─ README.md
```

#### Database
Create a database named sg_property_db in MySQL database
```
CREATE DATABASE sg_property_db;
```

# Usage
#### Ensure virtual environment is activate
```
.\sg_property_env\Scripts\activate
```

#### Running scripts
```
cd python_src
python ./read_data_to_db.py
python ./preprocess_data.py
```

Other mode
```
python ./preprocess_data.py --api=False
```

Get new one map api key
```
python ./get_onemap_token.py
```

# Explaination

1. read_data_to_db.py script reads the 'hdb_resale.csv' and create a table named 'hdb_resale'. It will also create 'hdb_rental' table as well as part of the csv to be processed.

2. read_data_to_db.py script also reads the 'child_care_data.geojson' and create a table named 'child_care'. It will also create 'elderly_care', 'hawker_centre', 'healthier_eateries' tables as well as part of the geojson to be processed. 

3. read_data_to_db.py script also processing kml file for 'lta_mrt' table was included in later stages.

4. preprocess_data.py script reads from the table named 'hdb_resale', cleaned the data and stored into table named 'hdb_resale_clean', further processes the data and stored the proceesed data into two tables named 'hdb_resale_avg_year' and 'hdb_resale_avg_town'. Similarly processing is performed on 'hdb_rental' table.

5. preprocess_data.py script also reads from the table named 'carpark_info', process x_coord, y_coord to lat, lon and split address into useful data (further improvement required, in order to use town column)

# Known Issue
Conversion to town from address consist of part 1 and part 2. 

Part 1 conversion is more accurate but time comsuming, and requires api update as it expires after 3 days

Part 2 conversion is not complete and contains some erroneous conversion (but minor issue, got converted to nearby town)

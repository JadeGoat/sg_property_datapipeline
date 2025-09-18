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
pip install python-dotenv
pip install python-dateutil
pip install pandas
```

#### Preparing .env file
Creating .env in python_src folder with the following field
```
DB_HOST = <to_fill_in_database_url>
DB_USER = <to_fill_in_database_username>
DB_PASSWORD = <to_fill_in_database_password>
DB_NAME = <to_fill_in_database_name>
```

#### Data
Copy the hdb resale flat prices to the data/ResaleFlatPrices folder


#### Folder Structure
```
├─ data
|  └─ ResaleFlatPrices
|     └─ data.csv
├─ python_src
|  ├─ .env
|  ├─ mysql_helper.py
|  ├─ preprocess_data.py
|  └─ read_csv_to_db.py
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
python ./read_csv_to_db.py
python ./preprocess_data.py
```

# Explaination

1. read_csv_to_db.py script reads the 'data.csv' and create a table named 'hdb_resale'

2. preprocess_data.py script reads from the table named 'hdb_resale', cleaned the data and stored into table named 'hdb_resale_clean', further processes the data and stored the proceesed data into two tables named 'hdb_resale_avg_year' and 'hdb_resale_avg_town'.
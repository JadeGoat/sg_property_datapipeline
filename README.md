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

#### Data
Copy the hdb resale flat prices to the data/ResaleFlatPrices folder
The folder structure should looks like this:
|- data
|  - ResaleFlatPrices
|    - data.csv
|- python_src
|  - .gitignore
|  - mysql_helper.py
|  - preprocess_data.py
|  - read_csv_to_db.py
|  - README.md
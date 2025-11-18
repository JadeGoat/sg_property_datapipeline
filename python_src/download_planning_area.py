import os
import json
import requests
from datetime import date
from dotenv import load_dotenv
import geopandas as gpd
from shapely.geometry import shape

import mysql.connector
from mysql_helper import get_db_config
from mysql_helper import create_table_for_geo_dataframes, insert_data_from_geo_dataframes

def fetch_general_planning_area(year, token, convert_geodataframe=True):
    url = f"https://www.onemap.gov.sg/api/public/popapi/getAllPlanningarea?year={year}"
    headers = {"Authorization": f"Bearer {token}"}

    # Make the request
    response = requests.get(url, headers=headers)

    if (response.status_code == 200):
        data = response.json()
        if 'SearchResults' in data.keys():
            planning_data = {}
            results = data["SearchResults"]

            for result in results:
                area = result['pln_area_n']
                print(f"Processing {area}...")

                if convert_geodataframe:
                    # Convert string => JSON
                    # Convert JSON => shapely geometries
                    # Convert shapely geometries => GeoDataFrames
                    geojson_geom = json.loads(result['geojson'])
                    area_data = shape(geojson_geom)
                    area_data = gpd.GeoDataFrame([{"geometry": area_data, "year": year}])
                else:
                    area_data = result['geojson']
                planning_data[area] = area_data

            return planning_data
        else:
            print("Invalid response structure")
    elif (response.status_code == 400):

        error_response = json.loads(response.text)
        key_phrase = "Allowed values are: "

        # Attempt to extract the recent year from error message
        if 'error' in error_response.keys() and key_phrase in error_response['error']:
            results = error_response['error'].split(key_phrase)
            if (len(results) == 2):
                year_list = [item.strip() for item in results[1].split(",")]
                year_list.sort()
                return year_list[-1]
    else:
        print(response.text)

    return None

def load_planning_area_into_database(planning_areas, db_config, table_name):

    # Connect to MySQL
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    create_table_for_geo_dataframes(cursor, table_name)
    for town_name, town_area in planning_areas.items():
        insert_data_from_geo_dataframes(town_name, town_area['geometry'][0], cursor, table_name)
    
    # Commit and close
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":

    # Main workflow
    load_dotenv()
    token = os.getenv('ONE_MAP_API_TOKEN')
    #token = get_token(EMAIL, PASSWORD)

    planning_areas = fetch_general_planning_area(date.today().year, token)
    if planning_areas is not None:
        if (len(planning_areas) == 4):
            year = planning_areas # For understanding purpose only
            planning_areas = fetch_general_planning_area(year, token)

    # Database details
    db_config = get_db_config()
    db_table_name = "planning_area"

    load_planning_area_into_database(planning_areas, db_config, db_table_name)
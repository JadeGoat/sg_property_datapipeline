import os
import json
import requests
import geopandas as gpd
from shapely.geometry import shape
import matplotlib.pyplot as plt
from dotenv import load_dotenv

def fetch_general_planning_area(year, token):
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

                # Convert string => JSON
                # Convert JSON => shapely geometries
                # Convert shapely geometries => GeoDataFrames
                geojson_geom = json.loads(result['geojson'])
                area_data = shape(geojson_geom)
                area_data = gpd.GeoDataFrame([{"geometry": area_data, "year": year}])
                planning_data[area] = area_data

            return planning_data
        else:
            #print(data['SearchResults'])
            print("Invalid response structure")
    else:
        print(response.text)
    return None

def fetch_master_planning_area(year, token):
    url = f"https://www.onemap.gov.sg/api/common/masterplanPlanningArea?year={year}"
    headers = {"Authorization": f"Bearer {token}"}

    # Make the request
    response = requests.get(url, headers=headers)

    if (response.status_code == 200):
        data = response.json()
        if 'MasterPlan' in data.keys():
            return gpd.GeoDataFrame.from_features(data["MasterPlan"])
        else:
            #print(data['SearchResults'])
            print("Invalid response structure")
    else:
        print(response.text)
    return None

def compare_generalplans(gdf1_dict, gdf2_dict, year1, year2):
    
    if gdf1_dict is not None and gdf2_dict is not None:

        sort_dict1 = dict(sorted(gdf1_dict.items()))
        sort_dict2 = dict(sorted(gdf2_dict.items()))
        zipped = list(zip(sort_dict1.items(), sort_dict2.items()))

        for gdf1, gdf2 in zipped:

            # Create plot
            _, ax = plt.subplots(1, 2, figsize=(14, 7))
            gdf1[1].plot(ax=ax[0], color="lightblue", edgecolor="black")
            gdf2[1].plot(ax=ax[1], color="lightgreen", edgecolor="black")
            
            # Set title
            ax[0].set_title(f"District Zone {year1} ({gdf1[0]})")
            ax[1].set_title(f"District Zone {year2} ({gdf2[0]})")
            plt.tight_layout()
            plt.savefig(f"../data/maps/district_zone_{gdf1[0].lower()}.png")
            plt.close()
            #plt.show()
    else:
        print("Missing plot data")

def compare_masterplans(gdf1, gdf2, year1, year2):

    if gdf1 is not None and gdf2 is not None:
        
        # Create plot
        _, ax = plt.subplots(1, 2, figsize=(14, 7))
        gdf1.plot(ax=ax[0], color="lightblue", edgecolor="black")
        gdf2.plot(ax=ax[1], color="lightgreen", edgecolor="black")
        
        # Set title
        ax[0].set_title(f"Master Plan {year1}")
        ax[1].set_title(f"Master Plan {year2}")
        plt.tight_layout()
        plt.show()
    else:
        print("Missing plot data")

if __name__ == "__main__":
    # Main workflow
    #token = get_token(EMAIL, PASSWORD)
    load_dotenv()
    token = os.getenv('ONE_MAP_API_TOKEN')

    general_plan_2014 = fetch_general_planning_area(2014, token)
    general_plan_2019 = fetch_general_planning_area(2019, token)
    compare_generalplans(general_plan_2014, general_plan_2019, 2014, 2019)

    #gdf_2014 = fetch_master_planning_area(2014, token)
    #gdf_2019 = fetch_master_planning_area(2019, token)
    #compare_masterplans(gdf_2014, gdf_2019, 2014, 2019)
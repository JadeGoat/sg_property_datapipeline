import os
import json
import requests
import pandas as pd
from dotenv import load_dotenv

def download_csv_from_data_gov_sg(dataset_id, csv_filename):
    
    # Initialize variables
    offset = 0
    limit = 10000
    result = pd.DataFrame()

    # First api call
    base_url = "https://data.gov.sg"
    url = base_url + "/api/action/datastore_search"
    url_full = url + "?resource_id="+ dataset_id + "&offset=" + str(offset) + "&limit=" + str(limit)
    response = requests.get(url_full)
    response_json = response.json()

    total = response_json['result']['total']
    if (limit > total):
        counter = total
    else:
        counter = limit

    # Subsequent api call
    while (len(response_json['result']['records']) > 0):
        
        print("Downloading " + str(counter) + "/" + str(total) + " rows of data...")
        if (response_json['result']['limit'] == 0):
            print(response_json['result']['fields'])
            result = pd.DataFrame(response_json['result']['records'])
        else:
            temp_result = pd.DataFrame(response_json['result']['records'])
            result = pd.concat([result, temp_result], ignore_index=True)

        # Next batch of records
        next_url = base_url + response_json['result']["_links"]["next"]
        response = requests.get(next_url)
        response_json = response.json()
        if (counter+limit > total):
            counter = total
        else:
            counter += limit

    result = result.drop(columns='_id')
    print(result.tail())
    result.to_csv(csv_filename, index=False)

def download_geojson_kml_from_data_gov_sg(dataset_id, filename):

    # First Api call
    url_full = "https://api-open.data.gov.sg/v1/public/api/datasets/" + dataset_id + "/poll-download"
    response = requests.get(url_full)

    # Get url from response to download
    json_data = response.json()
    if (("code" in json_data.keys()) and (json_data['code'] != 0)):
        print(json_data['errMsg'])
        exit(1)
    elif (len(json_data) == 0):
        print("Invalid payload")
        exit(1)

    # Second Api call to download payload
    if (("data" in json_data.keys()) and ('url' in json_data['data'].keys())):
        url = json_data['data']['url']
        response = requests.get(url)
        
        extension = os.path.splitext(filename)[1]
        if extension == ".geojson":
            # Save goejson file
            json_data = response.json()
            with open(filename, "w") as f:
                json.dump(json_data, f)

        elif extension == ".kml":
            # Save kml file
            kml_data = response.text
            with open(filename, "w") as f:
                f.write(kml_data)
        else:
            print("Invalid extension")

    else:
        print("Invalid payload")
        print(json_data.keys())
        print(json_data)
    
def download_data_from_datamall_lta(csv_filename):

    load_dotenv()
    acct_key = os.getenv('DATAMALL_ACCT_TOKEN') 
    headers = {
        'AccountKey': acct_key,
        'accept': 'application/json'
    }

    # Initialize variables
    skip = 0
    batch_size = 500
    result = pd.DataFrame()

    while True:

        # Making the api call
        url = f"https://datamall2.mytransport.sg/ltaodataservice/BusStops?$skip={skip}"
        response = requests.get(url, headers=headers)

        # Read data per api call and concat to dataframe
        if response.status_code == 200:
            data = response.json()
            
            # Exit when no more data
            if not data['value']:
                break
            
            if 'value' in data.keys():
                temp_result = pd.DataFrame(data['value'])
                result = pd.concat([result, temp_result], ignore_index=True)
        else:
            print(f"Error: {response.status_code}")
        
        # Increase skip counter, for next api call in next batch 
        skip += batch_size

    print(result.tail())
    result.to_csv(csv_filename, index=False)

if __name__ == "__main__":

    # Using data.gov api for csv type
    dataset_id_csv_array = [
        "d_23f946fa557947f93a8043bbef41dd09",
        "d_c9f57187485a850908655db0e8cfe651",
        "d_8b84c4ee58e3cfc0ece0d773c8ca6abc",
    ]
    csv_filename_array = [
        "carpark_data.csv",
        "hdb_rental_data.csv",
        "hdb_resale_data.csv",
    ]

    # Using data.gov api for geojson
    dataset_id_geojson_array = [
        "d_5d668e3f544335f8028f546827b773b4",
        "d_f0fd1b3643ed8bd34bd403dedd7c1533",
        "d_4a086da0a5553be1d89383cd90d07ecd",
        "d_2925c2ccf75d1c135c2d469e0de3cee6",
        "d_f820139ee3b0865b5512cf61ab7d1122",
    ]
    geojson_kml_filename_array = [
        "child_care_data.geojson",
        "elderly_care_data.geojson",
        "hawker_centre_data.geojson",
        "healthier_eateries_data.geojson",
        "lta_mrt.kml"
    ]

    # Using lta datamall api for csv type
    datamall_filename_array = [
        "busstop_data.csv",
    ]

    for filename, dataset_id in zip(csv_filename_array, dataset_id_csv_array):
        
        # Append filename to working directory
        csv_filename = os.path.join(os.getcwd(), "..", "data", filename)

        print("Downloading " + filename + "...")
        download_csv_from_data_gov_sg(dataset_id, csv_filename)

    
    for filename, dataset_id in zip(geojson_kml_filename_array, dataset_id_geojson_array):
        
        # Append filename to working directory
        csv_filename = os.path.join(os.getcwd(), "..", "data", filename)

        print("Downloading " + filename + "...")
        download_geojson_kml_from_data_gov_sg(dataset_id, csv_filename)
    
    for filename in datamall_filename_array:

        # Append filename to working directory
        csv_filename = os.path.join(os.getcwd(), "..", "data", filename)

        print("Downloading " + filename + "...")
        download_data_from_datamall_lta(csv_filename)
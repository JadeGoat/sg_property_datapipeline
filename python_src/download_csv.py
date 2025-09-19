import os
import requests
import pandas as pd

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

    # Subsuquent api call
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

if __name__ == "__main__":

    dataset_id_array = [
        "d_23f946fa557947f93a8043bbef41dd09",
        "d_c9f57187485a850908655db0e8cfe651",
        "d_8b84c4ee58e3cfc0ece0d773c8ca6abc",
    ]
    csv_filename_array = [
        "carpark_data.csv",
        "hdb_rental_data.csv",
        "hdb_resale_data.csv",
    ]

    for filename, dataset_id in zip(csv_filename_array, dataset_id_array):
        
        # Append filename to working directory
        csv_filename = os.path.join(os.getcwd(), "..", "data", filename)

        print("Downloading " + filename + "...")
        download_csv_from_data_gov_sg(dataset_id, csv_filename)

    
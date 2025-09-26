import os
import requests
from dotenv import load_dotenv

if __name__ == "__main__":

    load_dotenv()
    token = os.getenv('ONE_MAP_API_TOKEN')
    acct_email = os.getenv('ONE_MAP_API_EMAIL')
    acct_password = os.getenv('ONE_MAP_API_PASSWORD')

    url = "https://www.onemap.gov.sg/api/auth/post/getToken"
    payload = {
                "email": acct_email,
                "password": acct_password,
              }

    # Make the request
    response = requests.post(url, json=payload)
    
    if (response.status_code == 200):
        data = response.json()
        if 'access_token' in data.keys():
            print(data['access_token'])
        else:
            print("Invalid response structure")
    else:
        print(response.text)

    
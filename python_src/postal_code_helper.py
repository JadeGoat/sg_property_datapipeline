import os
import requests
from dotenv import load_dotenv

postal_prefix_to_town = {
    # Central Area
    "01": "Central Area", "02": "Central Area", "03": "Central Area", "04": "Central Area",
    "05": "Central Area", "06": "Central Area", "07": "Central Area", "08": "Central Area",
    "09": "Central Area", "10": "Central Area", "17": "Central Area", "18": "Central Area",
    "19": "Central Area", "20": "Central Area", "21": "Central Area", "22": "Central Area",
    "23": "Central Area", "28": "Central Area", "29": "Central Area", "30": "Central Area",
    # Clementi
    "11": "Clementi", "12": "Clementi", "13": "Clementi",
    # Queenstown
    "14": "Queenstown", "16": "Queenstown",
    # Bukit Merah (resolved overlap)
    "15": "Bukit Merah",
    # Bukit Timah (resolved overlap)
    "240": "Bukit Timah", "241": "Bukit Timah", "242": "Bukit Timah", "243": "Bukit Timah",
    "244": "Bukit Timah", "245": "Bukit Timah", "246": "Bukit Timah", "247": "Bukit Timah",
    "248": "Bukit Timah", "249": "Bukit Timah",
    # Bishan  (resolved overlap)
    "579": "Bishan", "570": "Bishan", "571": "Bishan",
    # Toa Payoh
    "31": "Toa Payoh", "32": "Toa Payoh",
    # Kallang/Whampoa
    "33": "Kallang/Whampoa", "34": "Kallang/Whampoa",
    # Geylang
    "38": "Geylang", "39": "Geylang", "40": "Geylang",
    # Marine Parade
    "41": "Marine Parade", "42": "Marine Parade", "43": "Marine Parade",
    # Bedok
    "44": "Bedok", "45": "Bedok", "46": "Bedok", "47": "Bedok", "48": "Bedok",
    # Tampines
    "49": "Tampines", "50": "Tampines",
    # Pasir Ris
    "51": "Pasir Ris", "52": "Pasir Ris", "53": "Pasir Ris",
    # Hougang
    "54": "Hougang",
    # Serangoon
    "55": "Serangoon",
    # Ang Mo Kio
    "56": "Ang Mo Kio", "57": "Ang Mo Kio",
    # Jurong East
    "60": "Jurong East", "61": "Jurong East",
    # Jurong West
    "62": "Jurong West", "63": "Jurong West", "64": "Jurong West",
    # Bukit Batok
    "65": "Bukit Batok", "66": "Bukit Batok",
    # Bukit Panjang
    "67": "Bukit Panjang",
    # Choa Chu Kang
    "68": "Choa Chu Kang", "69": "Choa Chu Kang", "70": "Choa Chu Kang", "71": "Choa Chu Kang",
    # Woodlands
    "72": "Woodlands", "73": "Woodlands", "74": "Woodlands",
    # Sembawang
    "75": "Sembawang", "76": "Sembawang",
    # Yishun
    "77": "Yishun", "78": "Yishun",
    # Sengkang
    "79": "Sengkang", "80": "Sengkang",
    # Punggol
    "81": "Punggol", "82": "Punggol"
}


def get_town_from_postal(postal_code):

    postal_code = str(postal_code)
    
    # Try 3 digit then with 2 digit
    for prefix_length in [3, 2]:
        prefix = postal_code[:prefix_length]

        # Lookup town using the 2/3 digit
        if prefix in postal_prefix_to_town:
            return postal_prefix_to_town[prefix].upper()
    
    return "Unknown"

def get_postal(x, y, token):
    #  OneMap Reverse Geocode endpoint
    url = f"https://www.onemap.gov.sg/api/public/revgeocodexy?location={x},{y}&buffer=40&addressType=All"

    # Set up headers with your token
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Make the request
    response = requests.get(url, headers=headers)
    data = response.json()

    # Extract town name from the response
    try:
        postal_code = data["GeocodeInfo"][0].get("POSTALCODE", "Unknown")
        latitude = data["GeocodeInfo"][0].get("LATITUDE", "Unknown")
        longitude = data["GeocodeInfo"][0].get("LONGITUDE", "Unknown")
        print("Postal code:", postal_code)
        #print("Latitude:", latitude)
        #print("Longitude:", longitude)
        
        return postal_code, latitude, longitude
    except (IndexError, KeyError):
        print("Warning: Could not retrieve postal code")
        return "Unknown", "Unknown", "Unknown"

if __name__ == "__main__":

    # Example usage
    load_dotenv()
    token = os.getenv('ONE_MAP_API_TOKEN')

    #postal_code = get_postal(29674.8, 40616.9, token)
    #postal_code = get_postal(29257.7, 34500.4, token)
    postal_code = get_postal(32444.5, 35453.7, token)
    #postal_code = get_postal(22359, 31801.6, token)
    #postal_code = get_postal(21005.6, 40580.3, token)

    town_name = get_town_from_postal(postal_code)
    print(town_name)


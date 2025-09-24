import os
import requests
from dotenv import load_dotenv

range_to_towns = {
    (0, 89): ["Central"],
    (90, 99): ["Bukit Merah"],
    (100, 116): ["Bukit Merah"],
    (117, 119): ["Queenstown"],
    (120, 129): ["Clementi"],
    (131, 131): ["Queenstown"],
    (132, 137): ["Clementi"],
    (138, 139): ["Queenstown"],
    (140, 149): ["Queenstown"],
    (150, 159): ["Bukit Merah"],
    (160, 169): ["Central"],
    (170, 178): ["Central"],
    (179, 199): ["Central"],
    (200, 249): ["Central"],
    (250, 259): ["Central"],
    (260, 266): ["Bukit Timah"],
    (267, 269): ["Bukit Timah"],
    (270, 276): ["Queenstown"],
    (277, 279): ["Bukit Timah"],
    (280, 289): ["Bukit Timah"],
    (290, 297): ["Bukit Timah"],
    (298, 298): ["Toa Payoh"],
    (299, 299): ["Bukit Timah"],
    (300, 307): ["Toa Payoh"],  # Novena
    (309, 310): ["Toa Payoh"],
    (310, 319): ["Toa Payoh"],
    (320, 322): ["Toa Payoh", "Kallang/Whampoa"],  # Balestier
    (323, 329): ["Toa Payoh", "Kallang/Whampoa"],  # Balestier
    (330, 331): ["Kallang/Whampoa"],  # Whampoa
    (332, 339): ["Kallang/Whampoa"],  # Whampoa
    (340, 349): ["Kallang/Whampoa"],
    (350, 359): ["Kallang/Whampoa"],
    (360, 369): ["Geylang"],
    (370, 379): ["Geylang"],
    (380, 389): ["Geylang"],
    (390, 399): ["Geylang"],
    (400, 409): ["Bedok"],
    (410, 419): ["Bedok"],
    (420, 429): ["Marine Parade"],
    (430, 439): ["Marine Parade"],
    (440, 449): ["Marine Parade"],
    (450, 459): ["Bedok"],
    (460, 469): ["Bedok"],
    (470, 479): ["Bedok"],
    (480, 489): ["Bedok"],
    (490, 499): ["Bedok", "Tampines"],
    (500, 509): ["Pasir Ris"],
    (510, 519): ["Pasir Ris"],
    (520, 529): ["Tampines"],
    (530, 539): ["Hougang"],
    (540, 544): ["Sengkang"],
    (545, 549): ["Sengkang", "Hougang"],
    (550, 559): ["Serangoon"],
    (560, 569): ["Ang Mo Kio", "Bishan"],
    (570, 579): ["Bishan"],
    (580, 585): ["Toa Payoh"],
    (586, 589): ["Bukit Timah"],
    (590, 590): ["Bukit Timah"],
    (591, 591): ["Bukit Timah"],
    (592, 599): ["Bukit Timah"],
    (600, 609): ["Jurong East"],
    (610, 619): ["Jurong West"],
    (620, 629): ["Jurong West"],
    (630, 632): ["Jurong West", "Bukit Batok"],
    (632, 632): ["Jurong West"],
    (633, 639): ["Jurong West", "Bukit Batok"],
    (640, 644): ["Jurong West"],
    (645, 650): ["Bukit Batok"],
    (650, 659): ["Bukit Batok"],
    (660, 669): ["Bukit Panjang"],
    (670, 679): ["Bukit Panjang"],
    (680, 689): ["Choa Chu Kang"],
    (690, 699): ["Tengah"],
    (700, 729): ["Woodlands"],
    (730, 739): ["Woodlands"],
    (740, 749): ["Yishun"],
    (750, 759): ["Yishun", "Sembawang"],
    (760, 769): ["Yishun"],
    (770, 779): ["Ang Mo Kio"],
    (780, 789): ["Ang Mo Kio"],
    (790, 799): ["Sengkang"],
    (800, 804): ["Punggol"],
    (805, 809): ["Ang Mo Kio"],
    (810, 819): ["Sembawang"],
    (820, 829): ["Punggol"],
    (830, 839): ["Sengkang"],
    (840, 849): ["Hougang"],
    (850, 859): ["Hougang"],
    (860, 869): ["Sengkang", "Hougang"],
    (870, 879): ["Sengkang"],
    (880, 889): ["Sengkang"],
    (890, 899): ["Punggol"],
    (900, 1000): ["Bedok"]
}

sg_town = ["Central", "Clementi", "Queenstown", "Bukit Merah", "Bukit Timah", "Bishan", "Ang Mo Kio",  
           "Toa Payoh", "Kallang/Whampoa", "Geylang", "Marine Parade", "Bedok", "Tampines", "Pasir Ris", "Hougang",   
           "Sengkang", "Serangoon", "Jurong East", "Bukit Batok", "Bukit Panjang", "Choa Chu Kang", "Tengah",   
           "Woodlands", "Sembawang", "Yishun", "Sengkang", "Punggol"]

def map_to_town(value):

    for town in sg_town:
        if town.upper() in str(value).upper():
            return town.upper()
    
    return "UNKNOWN"

def get_town_from_postal(postal_code):

    # Return ["UNKNOWN"] when postal_code is not a integer
    try:
        int(postal_code)
    except:
        return '["UNKNOWN"]'
    
    # Proceed with conversion
    postal_code = str(postal_code)
    prefix = int(postal_code[:3])

    # Lookup town within 
    for (start, end), towns in range_to_towns.items():
        if prefix in (start, end + 1):
            return str(towns).upper()
    
    return '["UNKNOWN"]'

def get_postal_from_svy21(x, y, token):
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

def get_postal_from_address(address, token):
    #  OneMap common endpoint
    url = "https://www.onemap.gov.sg/api/common/elastic/search"

    # Set up headers with your token
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Set up parameters
    params = {
        "searchVal": address,
        "returnGeom": "Y",
        "getAddrDetails": "Y",
        "pageNum": 1
    }

    # Make the request
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    print(data)
    try:
        postal_code = data["results"][0]["POSTAL"]
        latitude = data["results"][0].get("LATITUDE", "Unknown")
        longitude = data["results"][0].get("LONGITUDE", "Unknown")
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

    #postal_code = get_postal_from_svy21(29674.8, 40616.9, token)
    #postal_code = get_postal_from_svy21(29257.7, 34500.4, token)
    postal_code = get_postal_from_svy21(32444.5, 35453.7, token)
    #postal_code = get_postal_from_svy21(22359, 31801.6, token)
    #postal_code = get_postal_from_svy21(21005.6, 40580.3, token)

    town_name = get_town_from_postal(postal_code)
    print(town_name)


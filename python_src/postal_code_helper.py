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
    "14": "Queenstown",
    "27": "Queenstown", # Ghim Moh Road
    # Bukit Merah
    "15": "Bukit Merah", "16": "Bukit Merah",
    # Bukit Timah
    "240": "Bukit Timah", "241": "Bukit Timah", "242": "Bukit Timah", "243": "Bukit Timah",
    "244": "Bukit Timah", "245": "Bukit Timah", "246": "Bukit Timah", "247": "Bukit Timah",
    "248": "Bukit Timah", "249": "Bukit Timah",
    "261": "Bukit Timah", # Farrer Road
    "591": "Bukit Timah", #@
    # Bishan
    "570": "Bishan", "571": "Bishan", "575": "Bishan", "576": "Bishan", "579": "Bishan",
    # Ang Mo Kio
    "560": "Ang Mo Kio", "561": "Ang Mo Kio", "562": "Ang Mo Kio", "563": "Ang Mo Kio", "569": "Ang Mo Kio",
    # Toa Payoh
    "310": "Toa Payoh", "311": "Toa Payoh", "312": "Toa Payoh", "313": "Toa Payoh",
    "340": "Toa Payoh", "360": "Toa Payoh", # Bidadari
    "350": "Toa Payoh", # Potong Pasir
    "361": "Toa Payoh", # Upper Aljunied Lane
    # Kallang/Whampoa
    "319": "Kallang/Whampoa", "320": "Kallang/Whampoa", "321": "Kallang/Whampoa", 
    "322": "Kallang/Whampoa", "323": "Kallang/Whampoa", 
    "328": "Kallang/Whampoa", "330": "Kallang/Whampoa", #@
    "331": "Kallang/Whampoa", "338": "Kallang/Whampoa", "339": "Kallang/Whampoa",
    # Geylang
    "370": "Geylang", "371": "Geylang", "372": "Geylang", # Circuit Road/Pipit Road???
    "380": "Geylang", "381": "Geylang", "389": "Geylang", 
    "390": "Geylang", "391": "Geylang", "392": "Geylang", #@
    "399": "Geylang",
    # Marine Parade
    "402": "Marine Parade", # Geylang Serai
    "420": "Marine Parade", # Joo Chiat Road
    "430": "Marine Parade", # Haig Road
    "431": "Marine Parade", "432": "Marine Parade", # Kampong Arang Road
    "437": "Marine Parade", "438": "Marine Parade", "439": "Marine Parade", 
    "440": "Marine Parade", "441": "Marine Parade",
    # Bedok
    "400": "Bedok", # Eunos Cresent
    "410": "Bedok", # Lengkong Tiga
    "411": "Bedok", # Jalan Tenaga
    "460": "Bedok", "461": "Bedok", "462": "Bedok", "463": "Bedok", "465": "Bedok", "466": "Bedok",
    "467": "Bedok", "468": "Bedok", "469": "Bedok", "470": "Bedok", "471": "Bedok",
    # Tampines
    "520": "Tampines", "521": "Tampines", "522": "Tampines", "523": "Tampines", "524": "Tampines", 
    "526": "Tampines", "527": "Tampines", "529": "Tampines",
    # Pasir Ris
    "500": "Pasir Ris", "509": "Pasir Ris", # Changi Village
    "510": "Pasir Ris", "511": "Pasir Ris", "519": "Pasir Ris",
    # Hougang
    "530": "Hougang", "531": "Hougang", "532": "Hougang", "538": "Hougang",
    # Sengkang
    "540": "Sengkang", "541": "Sengkang", "542": "Sengkang", #@
    "544": "Sengkang", "545": "Sengkang",
    "546": "Sengkang", #@
    "790": "Sengkang", #@
    # Serangoon
    "550": "Serangoon", "551": "Serangoon", "552": "Serangoon", "555": "Serangoon", "556": "Serangoon",
    # Jurong East
    "600": "Jurong East", "601": "Jurong East", "603": "Jurong East", 
    "605": "Jurong East", #@
    "609": "Jurong East",
    # Jurong West
    "610": "Jurong West", "611": "Jurong West", "614": "Jurong West", #@
    "632": "Jurong West", # Upper Jurong Road
    "640": "Jurong West", "641": "Jurong West", "642": "Jurong West", "643": "Jurong West",
    # Bukit Batok
    "650": "Bukit Batok", "651": "Bukit Batok", "652": "Bukit Batok", "653": "Bukit Batok", 
    "655": "Bukit Batok", "657": "Bukit Batok", "659": "Bukit Batok",
    # Bukit Panjang
    "670": "Bukit Panjang", "671": "Bukit Panjang", 
    "672": "Bukit Panjang", #@
    "678": "Bukit Panjang",
    "679": "Bukit Panjang", #@
    "688": "Bukit Panjang", # Teck Whye Lane
    # Choa Chu Kang
    "680": "Choa Chu Kang", "681": "Choa Chu Kang", "682": "Choa Chu Kang", "689": "Choa Chu Kang",
    # Tengah
    "690": "Tengah", "691": "Tengah", "692": "Tengah",
    # Woodlands
    "730": "Woodlands", "731": "Woodlands", "732": "Woodlands", "733": "Woodlands", 
    "739": "Woodlands", "738": "Woodlands",
    # Sembawang
    "750": "Sembawang", 
    "751": "Sembawang", "752": "Sembawang", "753": "Sembawang", #@
    "759": "Sembawang",
    # Yishun
    "760": "Yishun", "761": "Yishun", "762": "Yishun",  "768": "Yishun", "769": "Yishun",
    # Punggol
    "820": "Punggol", "821": "Punggol", "822": "Punggol", "823": "Punggol", "824": "Punggol", 
    "829": "Punggol"
}

sg_town = ["Central Area", "Clementi", "Queenstown", "Bukit Merah", "Bukit Timah", "Bishan", "Ang Mo Kio",  
           "Toa Payoh", "Kallang/Whampoa", "Geylang", "Marine Parade", "Bedok", "Tampines", "Pasir Ris", "Hougang",   
           "Sengkang", "Serangoon", "Jurong East", "Bukit Batok", "Bukit Panjang", "Choa Chu Kang", "Tengah",   
           "Woodlands", "Sembawang", "Yishun", "Sengkang", "Punggol"]

def map_to_town(value):

    for town in sg_town:
        if town.upper() in str(value).upper():
            return town.upper()
    
    return "Unknown"

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


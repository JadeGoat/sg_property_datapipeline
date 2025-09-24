import os
import requests
from dotenv import load_dotenv

postal_prefix_to_town = {
    # Central
    "01": "Central", "02": "Central", "03": "Central", "04": "Central",
    "05": "Central", "06": "Central", "07": "Central", "08": "Central",
    "09": "Central", "10": "Central", "17": "Central", "18": "Central",
    "19": "Central", "20": "Central", "21": "Central", "22": "Central",
    "23": "Central", "28": "Central", "29": "Central", "30": "Central",
    "229": "Central",
    "247": "Central", "248": "Central", "249": "Central",
    "259": "Central",
    # Clementi
    "11": "Clementi", "12": "Clementi", "13": "Clementi",
    # Queenstown
    "14": "Queenstown",
    "27": "Queenstown", # Ghim Moh Road
    # Bukit Merah
    "15": "Bukit Merah", "16": "Bukit Merah",
    "088": "Bukit Merah", # Raeburn Park
    "090": "Bukit Merah", # Telok Blangah Rise/Crescent
    "098": "Bukit Merah", # Wishart Road
    "099": "Bukit Merah", # Harbourfront place
    "100": "Bukit Merah", "101": "Bukit Merah", "102": "Bukit Merah", # Telok Blangah Street
    "103": "Bukit Merah", "109": "Bukit Merah", # Depot Road
    # Bukit Timah
    "240": "Bukit Timah", "241": "Bukit Timah", "242": "Bukit Timah", "243": "Bukit Timah",
    "244": "Bukit Timah", "245": "Bukit Timah", "246": "Bukit Timah", 
    "261": "Bukit Timah", # Farrer Road
    "277": "Bukit Timah", #@
    "278": "Bukit Timah", #@
    "286": "Bukit Timah", # Fairways Drive
    "287": "Bukit Timah", # Turf Club Road
    "288": "Bukit Timah", # Linden Drive
    "289": "Bukit Timah", # Bukit Tinggi Road
    "297": "Bukit Timah", # Plymouth Avenue
    "299": "Bukit Timah", # Duneran Close
    "589": "Bukit Timah", "590": "Bukit Timah", "591": "Bukit Timah", #@
    "597": "Bukit Timah", #@
    "599": "Bukit Timah", #@
    # Bishan
    "570": "Bishan", "571": "Bishan", "572": "Bishan", 
    "575": "Bishan", "576": "Bishan", "579": "Bishan",
    # Ang Mo Kio
    "560": "Ang Mo Kio", "561": "Ang Mo Kio", "562": "Ang Mo Kio", "563": "Ang Mo Kio", 
    "568": "Ang Mo Kio", "569": "Ang Mo Kio",
    "809": "Ang Mo Kio", # Seletar Hills Estate
    # Toa Payoh
    "298": "Toa Payoh", # Thomson Road
    "310": "Toa Payoh", "311": "Toa Payoh", "312": "Toa Payoh", "313": "Toa Payoh",
    "340": "Toa Payoh", "341": "Toa Payoh", "360": "Toa Payoh", # Bidadari
    "347": "Toa Payoh", # Tai Thong Crescent
    "350": "Toa Payoh", # Potong Pasir
    "359": "Toa Payoh", # Jalan Lateh
    "361": "Toa Payoh", "367": "Toa Payoh", # Upper Aljunied Lane
    # Kallang/Whampoa
    "319": "Kallang/Whampoa", "320": "Kallang/Whampoa", "321": "Kallang/Whampoa", 
    "322": "Kallang/Whampoa", "323": "Kallang/Whampoa", 
    "328": "Kallang/Whampoa", "330": "Kallang/Whampoa", #@
    "331": "Kallang/Whampoa", "338": "Kallang/Whampoa", "339": "Kallang/Whampoa",
    # Geylang
    "348": "Geylang", #@
    "370": "Geylang", "371": "Geylang", "372": "Geylang", # Circuit Road/Pipit Road???
    "380": "Geylang", "381": "Geylang", "389": "Geylang", 
    "390": "Geylang", "391": "Geylang", "392": "Geylang", #@
    "399": "Geylang",
    "401": "Geylang", # Eunos Crescent
    # Marine Parade
    "402": "Marine Parade", # Geylang Serai
    "420": "Marine Parade", # Joo Chiat Road
    "430": "Marine Parade", # Haig Road
    "431": "Marine Parade", "432": "Marine Parade", # Kampong Arang Road
    "437": "Marine Parade", "438": "Marine Parade", "439": "Marine Parade", 
    "440": "Marine Parade", "441": "Marine Parade", "449": "Marine Parade",
    # Bedok
    "400": "Bedok", # Eunos Cresent
    "410": "Bedok", # Lengkong Tiga
    "411": "Bedok", # Jalan Tenaga
    "415": "Bedok", # Kaki Bukit Road
    "456": "Bedok", # Palm Avenue
    "458": "Bedok", # Frankel Avenue
    "460": "Bedok", "461": "Bedok", "462": "Bedok", "463": "Bedok", "465": "Bedok", "466": "Bedok",
    "467": "Bedok", "468": "Bedok", "469": "Bedok", "470": "Bedok", "471": "Bedok",
    # Tampines
    "486": "Tampines", # Upper Changi Road
    "520": "Tampines", "521": "Tampines", "522": "Tampines", "523": "Tampines", "524": "Tampines", 
    "526": "Tampines", "527": "Tampines", "529": "Tampines",
    # Pasir Ris
    "500": "Pasir Ris", "509": "Pasir Ris", # Changi Village
    "508": "Pasir Ris", # Changi Grove
    "510": "Pasir Ris", "511": "Pasir Ris", "519": "Pasir Ris",
    # Hougang
    "530": "Hougang", "531": "Hougang", "532": "Hougang", "538": "Hougang",
    "534": "Hougang", # Upper Serrangoon Road
    "536": "Hougang", #@
    "537": "Hougang", # Kensington Square
    "549": "Hougang", # Flower Road
    # Sengkang
    "540": "Sengkang", "541": "Sengkang", "542": "Sengkang", "543": "Sengkang", #@
    "544": "Sengkang", #@@ Mix serangoon & sengkang
    "545": "Sengkang", #@@ Mix serangoon & sengkang
    "546": "Sengkang", #@
    "790": "Sengkang", "791": "Sengkang", # Fernvale Street
    # Serangoon
    "550": "Serangoon", "551": "Serangoon", "552": "Serangoon", 
    "554": "Serangoon", "555": "Serangoon", "556": "Serangoon",
    # Jurong East
    "598": "Jurong East", #@
    "600": "Jurong East", "601": "Jurong East", "602": "Jurong East",  "603": "Jurong East", 
    "605": "Jurong East", #@
    "609": "Jurong East",
    # Jurong West
    "610": "Jurong West", "611": "Jurong West", "614": "Jurong West", #@
    "632": "Jurong West", # Upper Jurong Road
    "640": "Jurong West", "641": "Jurong West", "642": "Jurong West", "643": "Jurong West", "644": "Jurong West",
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
    "680": "Choa Chu Kang", "681": "Choa Chu Kang", "682": "Choa Chu Kang", "683": "Choa Chu Kang", 
    "689": "Choa Chu Kang",
    # Tengah
    "690": "Tengah", "691": "Tengah", "692": "Tengah",
    # Woodlands
    "730": "Woodlands", "731": "Woodlands", "732": "Woodlands", "733": "Woodlands", 
    "737": "Woodlands", "738": "Woodlands", "739": "Woodlands", 
    # Sembawang
    "750": "Sembawang", 
    "751": "Sembawang", "752": "Sembawang", "753": "Sembawang", #@
    "757": "Sembawang", "759": "Sembawang",
    # Yishun
    "760": "Yishun", "761": "Yishun", "762": "Yishun", "763": "Yishun", 
    "768": "Yishun", "769": "Yishun",
    # Punggol
    "820": "Punggol", "821": "Punggol", "822": "Punggol", "823": "Punggol", "824": "Punggol", 
    "829": "Punggol"
}

range_to_towns = {
    (0, 89): ["Central"],
    (90, 99): ["Central", "Bukit Merah"],
    (100, 119): ["Central", "Bukit Merah"],
    (120, 129): ["Clementi"],
    (130, 139): ["Clementi"],
    (140, 149): ["Clementi", "Queenstown"],
    (150, 159): ["Queenstown", "Bukit Merah"],
    (160, 169): ["Central", "Bukit Merah"],
    (170, 178): ["Central"],
    (179, 199): ["Central"],
    (200, 249): ["Central"],
    (250, 259): ["Central"],
    (260, 266): ["Queenstown"],
    (267, 269): ["Queenstown", "Bukit Timah"],
    (270, 279): ["Bukit Timah"],
    (280, 289): ["Bukit Timah"],
    (290, 299): ["Bukit Timah"],
    (300, 309): ["Kallang/Whampoa"],
    (310, 319): ["Kallang/Whampoa", "Toa Payoh"], 
    (320, 329): ["Kallang/Whampoa", "Toa Payoh"],
    (320, 331): ["Kallang/Whampoa", "Toa Payoh"],
    (332, 339): ["Kallang/Whampoa", "Toa Payoh", "Bishan"],
    (340, 349): ["Kallang/Whampoa", "Geylang"],
    (350, 359): ["Kallang/Whampoa", "Geylang"],
    (360, 369): ["Geylang"],
    (370, 379): ["Geylang"],
    (380, 389): ["Geylang"],
    (390, 399): ["Kallang/Whampoa", "Geylang"],
    (400, 409): ["Geylang"],
    (410, 419): ["Geylang", "Kallang/Whampoa"],
    (420, 429): ["Geylang", "Marine Parade"],
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
    (540, 549): ["Sengkang"],
    (550, 559): ["Serangoon"],
    (560, 569): ["Ang Mo Kio", "Bishan"],
    (570, 579): ["Bishan"],
    (580, 585): ["Toa Payoh"],
    (586, 589): ["Toa Payoh", "Bukit Timah"],
    (590, 590): ["Toa Payoh", "Bukit Timah", "Kallang/Whampoa"],
    (591, 591): ["Bukit Timah"],
    (592, 599): ["Toa Payoh", "Bukit Timah", "Kallang/Whampoa"],
    (600, 609): ["Jurong East"],
    (610, 619): ["Jurong West"],
    (620, 629): ["Jurong West"],
    (630, 631): ["Jurong West", "Bukit Batok"],
    (632, 632): ["Jurong West"],
    (633, 639): ["Jurong West", "Bukit Batok"],
    (640, 644): ["Jurong West"],
    (645, 649): ["Bukit Batok"],
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
    (800, 809): ["Punggol"],
    (810, 819): ["Sembawang"],
    (820, 829): ["Punggol"],
    (830, 839): ["Sengkang"],
    (840, 849): ["Hougang"],
    (850, 859): ["Hougang"],
    (860, 869): ["Sengkang","Hougang"],
    (870, 879): ["Sengkang"],
    (880, 889): ["Sengkang"],
    (890, 899): ["Punggol"],
    (900, 999): ["Bedok"]
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

def get_town_from_postal_old(postal_code):

    postal_code = str(postal_code)
    
    # Try 3 digit then with 2 digit
    for prefix_length in [3, 2]:
        prefix = postal_code[:prefix_length]

        # Lookup town using the 2/3 digit
        if prefix in postal_prefix_to_town:
            return postal_prefix_to_town[prefix].upper()
    
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

    # Lookup town within range
    for (start, end), towns in range_to_towns.items():
        if prefix in range(start, end + 1):
            if start==590:
                print(postal_code, prefix, start, end, towns)
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


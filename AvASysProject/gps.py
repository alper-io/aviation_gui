import json
from urllib.request import urlopen


class GPSModule:

    def getMyLoc(self):
        urlopen("http://ipinfo.io/json")
        data = json.load(urlopen("http://ipinfo.io/json"))
        lat = data['loc'].split(',')[0]
        lon = data['loc'].split(',')[1]
        print(lat, lon)
        return lat, lon

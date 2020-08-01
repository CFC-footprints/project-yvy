import requests
import os


def weather_request(lat, lon, start, end):
    API_KEY = os.environ['API_KEY_WEATHER']
    URL = "https://api.meteostat.net/v2/point/daily" # Max 380 days   
    headers = {
        "x-api-key": API_KEY
    }
    params = {
        "lat": lat,
        "lon": lon,
        "start": start,
        "end": end
    }
    res = requests.get(url=URL, headers=headers, params=params)
    return (res.json())

if __name__ == "__main__":
    print ("Start...")
    lat = "-33.416889"
    lon = "-70.606705"
    start = "2020-06-01"
    end = "2020-07-29"
    res = weather_request(lat, lon, start, end)
    data = res["data"]
    print (res)
    #example = data[0]
    #print (example)

import requests
import geocoder
import json
import urllib

# Get current location
g = geocoder.ip('me')

observer_lat = g.latlng[0]
observer_long = g.latlng[1]
iss_id = '25544'


def get_satellite_position(sat_id, lat, long):
    api_key = "DFCSDG-RXT46V-EQXF6C-56H2"
    url = f"https://api.n2yo.com/rest/v1/satellite/positions/{sat_id}/{lat}/{long}/0/2/&apiKey={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        satellite_data = response.json()
        json.dumps(satellite_data, indent=4)
        return satellite_data
    
# get_satellite_position(iss_id, observer_lat, observer_long)
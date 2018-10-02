import geopy.distance
import requests
import os
import time
import pytz
import datetime as dt

STATION_INFO_URL = "https://gbfs.citibikenyc.com/gbfs/en/station_information.json"
STATION_STATUS_URL = "https://gbfs.citibikenyc.com/gbfs/en/station_status.json"
#MY_COORDS =
DIST_THRESH_KM = 0.3

OUTPUT_FILE = './output.csv'

stations_info = requests.get(STATION_INFO_URL).json()['data']['stations']

# station_subset = {s['station_id'] for s in stations_info if 
    # geopy.distance.geodesic((s['lat'], s['lon']), MY_COORDS) < DIST_THRESH_KM}
station_subset = {s['station_id'] for s in stations_info}

fields = ['station_id', 'num_bikes_available', 'num_docks_available', 'last_reported']

if not os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, 'w') as f:
        f.write(','.join(['timestamp'] + fields) + '\n')

while True:
    wakeup = dt.datetime.now(pytz.utc)

    stations_status = requests.get(STATION_STATUS_URL).json()['data']['stations']

    with open(OUTPUT_FILE, 'a') as f:
        for s in stations_status:
            f.write('{},'.format(wakeup))
            f.write(','.join(str(s[f]) for f in fields))
            f.write('\n')

    time.sleep(15)

import geopy.distance
import requests
import os
import time
import datetime as dt

STATION_INFO_URL = "https://gbfs.citibikenyc.com/gbfs/en/station_information.json"
STATION_STATUS_URL = "https://gbfs.citibikenyc.com/gbfs/en/station_status.json"
#MY_COORDS = 
DIST_THRESH_KM = 0.3

OUTPUT_FOLDER = './output'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

stations_info = requests.get(STATION_INFO_URL).json()['data']['stations']

# station_subset = {s['station_id'] for s in stations_info if 
    # geopy.distance.geodesic((s['lat'], s['lon']), MY_COORDS) < DIST_THRESH_KM}
station_subset = {s['station_id'] for s in stations_info}

while True:
    print(dt.datetime.now())
    stations_status = requests.get(STATION_STATUS_URL).json()['data']['stations']

    for s in stations_status:
        sid = s['station_id']
        if sid in station_subset:
            with open(os.path.join(OUTPUT_FOLDER, sid + '.csv'), 'a') as f:
                f.write('{},{}\n'.format(s['last_reported'], s['num_bikes_available']))

    time.sleep(5)

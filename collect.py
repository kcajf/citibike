import requests
import os
import time
import datetime as dt

STATION_INFO_URL = "https://gbfs.citibikenyc.com/gbfs/en/station_information.json"
STATION_STATUS_URL = "https://gbfs.citibikenyc.com/gbfs/en/station_status.json"

FIELDS = [
    'station_id', 
    'num_bikes_available',
    'num_ebikes_available',
    'num_bikes_disabled',
    'num_docks_available',
    'num_docks_disabled',
    'is_installed',
    'is_renting',
    'last_reported',
]

OUTPUT_FILE = './output.csv'

def run_collector():
    if not os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'w') as f:
            f.write(','.join(['timestamp'] + FIELDS) + '\n')

    prev_last_updated = 0
    
    while True:
        try:
            stations_status = requests.get(STATION_STATUS_URL).json()

            last_updated = int(stations_status['last_updated'])

            if last_updated == prev_last_updated:
                continue

            print(dt.datetime.now(), dt.datetime.fromtimestamp(prev_last_updated), dt.datetime.fromtimestamp(last_updated))
            with open(OUTPUT_FILE, 'a') as h:
                for s in stations_status['data']['stations']:
                    h.write(str(last_updated))
                    h.write(',')
                    for f in FIELDS:
                        h.write(str(s[f]))
                        if f != FIELDS[-1]:
                            h.write(',')
                    h.write('\n')

            prev_last_updated = last_updated

        except Exception as e:
            print(e)

        time.sleep(6)

if __name__ == "__main__":
    run_collector()
#
# Brandon Gant
# Created: 2020-06-09
#
# Espressif ESP32-PICO-KIT_V4.1 board with ESP32-PICO-D4 chip 
# Milone Standard eTape assembly / 18-inch / Voltage divider / PN 12110215TC-AH
#
# Files required to run this script:
#    boot.py (boot_with_wifi.py)
#    key_store.py
#    client_id.py
#    soft_wdt.py
#    main.py (main_influxdb_etape.py)
#    Milone_eTape.py
#

from soft_wdt import wdt_feed, WDT_CANCEL  # Initialize Watchdog Timer

from machine import reset, Pin
from time import sleep
import urequests

import key_store
from client_id import client_id
from sys import exit

import Milone_eTape

# Get Unique Machine ID
from client_id import client_id
print('Client ID:', client_id)

# Get InfluxDB server:port:database:name from key_store.db
# i.e. influxdb.localdomain:8086:Garage:DHT22
server,port,database,name = key_store.get('influxdb').split(':')
url = 'http://%s:%s/write?db=%s' % (server,port,database)
print(url)

sleep_interval = 10   # Seconds

def main():
    print('=' * 45)
    print()

    # Read the eTape
    water = Milone_eTape.inches()
    print('Inches of Water: %.01f' % (water)

    # Send the Data to Server
    data = "name,device=%s inches=%.01f" % (client_id, inches)
    response = urequests.post(url,data=data)
    #print('STATUS:', response.status_code)
    if '204' in str(response.status_code):  # HTTP Status 204 (No Content) indicates server successfull fulfilled request with no response content
        print('Upload: Success')
        print()
    else:
        print('Upload: Failed')
        sleep(sleep_interval)
        reset()


while True:
    try:
        main()
        wdt_feed(sleep_interval * 2)  # Keep Watchdog Timer from resetting device for 2x sleep_interval
        sleep(sleep_interval)
    except KeyboardInterrupt:
        wdt_feed(WDT_CANCEL)  # Cancel/Disable Watchdog Timer when Ctrl+C pressed
        exit()
    except:
        sleep(sleep_interval)
        reset()

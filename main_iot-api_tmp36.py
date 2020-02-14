#
# Brandon Gant
# Created: 2019-12-17
# Updated: 2020-02-14
#
# Espressif ESP8266-DevKitc_V1 board with ESP-WROOM-02D chip
# Espressif ESP32-PICO-KIT_V4.1 board with ESP32-PICO-D4 chip 
# TMP36 temperature sensor with Vout connected to ADC pin
#
# Files required to run this script:
#    boot.py (boot_with_wifi.py)
#    key_store.py
#    client_id.py
#    soft_wdt.py
#    main.py (main_iot-api_tmp36.py)
#    AnalogDevices_TMP36.py
#    iot-api.py
#

from soft_wdt import wdt_feed, WDT_CANCEL  # Initialize Watchdog Timer

from machine import reset
from time import sleep

import key_store
from iot_api import iot_api
from client_id import client_id
import AnalogDevices_TMP36 as tmp36
from sys import exit
from uos import uname

# Get Unique Machine ID
from client_id import client_id
print('Client ID:', client_id)

# Get iot-api server:port from key_store.db
server,port = key_store.get('iot-api').split(':')

if server == 'api.thingspeak.com':
    client_id = key_store.get('thingspeak_api_key')
    if not client_id:
        client_id = input('Enter ThingSpeak write_api_key: ')
        key_store.set('thingspeak_api_key', 'client_id')

# ThingSpeak free tier limited to 15 seconds between data updates
sleep_interval = 30   # Seconds


def main():
    print('=============================================')
    print()

    # Read the Temperature
    hardware = uname().sysname
    if 'esp32' in hardware:
        field1 = round(tmp36.read_temp(37,'F'), 1)
    elif 'esp8266' in hardware:
        field1 = round(tmp36.read_temp(0,'F'), 1)
    print('Temperature Reading: %sF' % field1)

    # Send the Data to Server
    response = iot_api(server, port, client_id, field1)
    if response:
        print('Status: Success')
        print()
    else:
        print('Status: Failed')
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


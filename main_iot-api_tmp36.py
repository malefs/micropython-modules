#
# Brandon Gant
# 2019-12-17
#
# Espressif ESP8266-DevKitc_V1 board with ESP-WROOM-02D chip
# Espressif ESP32-PICO-KIT_V4.1 board with ESP32-PICO-D4 chip 
# TMP36 temperature sensor with Vout connected to ADC pin
#

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
periodic_reset = 720  # reset every 6 hours (21600 seconds) just in case / 15x1440 / 30x720 / 60x360


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


counter = 0
while True:
    try:
        main()
        counter += 1
        sleep(0.5)  # Give a half-second to display output before device sleeps
        sleep(sleep_interval)

        if counter > periodic_reset:  # Reset on a schedule just in case
            reset() 
    except:
        sleep(sleep_interval)
        reset()


#
# Brandon Gant
# Created: 2019-12-17
# Updated: 2020-09-27
#
# Espressif ESP8266-DevKitc_V1 board with ESP-WROOM-02D chip
# Espressif ESP32-PICO-KIT_V4.1 board with ESP32-PICO-D4 chip 
# TMP36 temperature sensor with Vout connected to ADC pin
#
# ESP32 Configuration:
#    esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
#    esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32-idf3-20200902-v1.13.bin
#    mpfshell
#    open ttyUSB0
#
#    put boot_with_wifi.py boot.py
#    put key_store.py
#    put soft_wdt.py
#
#    put main_iot-api_tmp36.py main.py
#    put client_id.py
#    put AnalogDevices_TMP36.py
#    put iot-api.py
#
#    repl
#    from machine import reset
#    reset()
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

# Get ADC Pin from key_store.db
if 'esp32' in uname().sysname:
    ADC_PIN = key_store.get('ADC_PIN')
    if ADC_PIN is None:
        key_store.set('ADC_PIN', input('Enter ADC Pin Number - '))
        reset()

# Get iot-api server:port from key_store.db
try:
    server,port = key_store.get('iot-api').split(':')
except:
    server = input('Enter iot-api server:port - ')
    key_store.set('iot-api', server)
    reset()

if server == 'api.thingspeak.com':
    client_id = key_store.get('thingspeak_api_key')
    if not client_id:
        client_id = input('Enter ThingSpeak write_api_key: ')
        key_store.set('thingspeak_api_key', 'client_id')

# ThingSpeak free tier limited to 15 seconds between data updates
sleep_interval = 30   # Seconds


def main():
    print('=' * 45)
    print()

    # Read the Temperature
    if 'esp32' in uname().sysname:
        field1 = round(tmp36.read_temp(int(ADC_PIN),'F'), 1)
    elif 'esp8266' in uname().sysname:
        field1 = round(tmp36.read_temp(0,'F'), 1)  # Only one ADC on PIN 0
    print('Temperature Reading: %sF' % field1)

    # Send the Data to Server
    response = iot_api(server, port, client_id, field1)
    if response:
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


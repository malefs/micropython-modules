#
# Brandon Gant
# Created: 2020-03-30
#
# Espressif ESP32-PICO-KIT_V4.1 board with ESP32-PICO-D4 chip 
# DHT22 temperature/humidity sensor
#
# Files required to run this script:
#    boot.py (boot_with_wifi.py)
#    key_store.py
#    client_id.py
#    soft_wdt.py
#    main.py (main_influxdb_dht22.py)
#

from soft_wdt import wdt_feed, WDT_CANCEL  # Initialize Watchdog Timer

import dht
from machine import reset, Pin
from time import sleep
import urequests

import key_store
from client_id import client_id
from sys import exit

# Get Unique Machine ID
from client_id import client_id
print('Client ID:', client_id)

# Get InfluxDB server:port:database:location from key_store.db
server,port,database,location = key_store.get('influxdb').split(':')
url = 'http://%s:%s/write?db=%s' % (server,port,database)
print(url)

sleep_interval = 30   # Seconds

# Any GPIO pin should work
sensor = dht.DHT22(Pin(18))

def main():
    print('=' * 45)
    print()

    # Read the Temperature and Humidity
    sensor.measure()
    temp_F = sensor.temperature() * 9/5 + 32  # Convert Celsius to Fahrenheit
    print('Temperature: %.01fC  RH: %.01f%%' % (temp_F, sensor.humidity()))

    # Send the Data to Server
    data = "DHT22,device=%s,location=%s temp_F=%.01f,humidity=%.01f" % (client_id, location, temp_F, sensor.humidity())
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


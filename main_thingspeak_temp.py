#
# Brandon Gant
# 2019-12-17
#
# Espressif ESP8266-DevKitc_V1 board with ESP-WROOM-02D chip
# Espressif ESP32-PICO-KIT_V4.1 board with ESP32-PICO-D4 chip 
# TMP36 temperature sensor with Vout connected to ADC pin
#

import key_store
import http_client
import tmp36
from time import sleep
from sys import exit
from machine import reset
from machine import lightsleep


# Get ThingSpeak API Key
import btree
f = open('key_store.db', 'r+b')
db = btree.open(f)
thingspeak_api_key = db[b'thingspeak_api_key'].decode('utf-8')
db.close()


server = 'api.thingspeak.com'

sleep_interval = 60   # Seconds
periodic_reset = 360  # with 60 second sleep, reset every 6 hours (just in case)


def main():
    print('=============================================')
    print()

    # Read the Temperature
    from uos import uname
    hardware = uname().sysname
    if 'esp32' in hardware:
        tempf = tmp36.read_temp(37,'F')
    elif 'esp8266' in hardware:
        tempf = tmp36.read_temp(0,'F')
    print('Temperature Reading: %sF' % tempf)

    # Create the HTTPS GET Request string
    get_request = 'GET /update?api_key=' + thingspeak_api_key + '&field1=' + str(tempf) + ' HTTP/1.0\r\n\r\n'
    get_request = str.encode(get_request)  # Convert Type str to bytes

    # Send the Data to ThingSpeak
    print('Sending Data To:', server)
    response_text = http_client.send_data(server, get_request)
    #print(response_text)

    status = [ line for line in response_text.split('\r\n') if "Status" in line ]
    if '200 OK' in status[0]:
        print('Status: Success')
        print()
    else:
        print('Status: Failed')
        sleep(sleep_interval)
        reset()


# ThingSpeak free tier limited to 15 seconds between data updates
counter = 0
while True:
    try:
        main()
        counter += 1
        sleep(0.5)  # Give a half-second to display output before device sleeps
        #lightsleep(sleep_interval * 1000)  # Milliseconds / No access to REPL while sleeping
        sleep(sleep_interval)

        if counter > periodic_reset:  # Reset on a schedule just in case
            reset() 
    except:
        sleep(sleep_interval)
        reset()


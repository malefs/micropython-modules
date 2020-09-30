#
# Brandon Gant
# Created: 2020-06-09
# Updated: 2020-09-30
#
# Espressif ESP32-PICO-KIT_V4.1 board with ESP32-PICO-D4 chip 
# Milone Standard eTape assembly / 18-inch / Voltage divider / PN 12110215TC-AH
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
#    put main_influxdb_etape.py main.py    
#    put client_id.py
#    put Milone_eTape.py
#    put urequests.py     <-- If TinyPICO
#    put TinyPICO_RGB.py  <-- If TinyPICO
#
#    repl   <-- Ctrl+] to exit repl back to mpfshell
#    from machine import reset
#    reset()
#

from soft_wdt import wdt_feed, WDT_CANCEL  # Initialize Watchdog Timer
wdt_feed(60)  # main.py script has 1 minute to initialize and loop before Watchdog timer resets device

from machine import reset
from time import sleep
from uos import uname
import urequests
import gc 

import key_store
from client_id import client_id
from sys import exit

import Milone_eTape

if 'TinyPICO' in uname().machine:
    import TinyPICO_RGB as led
    led.off()

# Get Unique Machine ID
from client_id import client_id

# Get ADC Pin from key_store.db
if 'esp32' in uname().sysname:
    if key_store.get('ADC_PIN') is None:
        key_store.set('ADC_PIN', input('Enter ADC Pin Number - '))
    ADC_PIN = key_store.get('ADC_PIN')

# Get InfluxDB server:port:database:measurement from key_store.db
# i.e. influxdb.localdomain:8086:Garage:DHT22
if key_store.get('influxdb') is None:
    print('Need to add settings to key_store.db...')
    key_store.set('influxdb', input('Enter InfluxDB server:port:database:measurement - '))
server,port,database,measurement = key_store.get('influxdb').split(':')

sleep_interval = 3  # Seconds

# Create database if it does not already exist (only works without InfluxDB  authentication)
#url = 'http://%s:%s/query' % (server,port)
#headers = {'Content-type': 'application/x-www-form-urlencoded'}
#data = 'q=SHOW DATABASES'
#response = urequests.post(url,headers=headers,data=data)
#if not database in response.text:
#    print('Creating Database: %s' % (database))
#    data = 'q=CREATE DATABASE "%s"' % (database)  # DROP DATABASE to remove
#    response = urequests.post(url,headers=headers,data=data)
#else:
#    print('Using Database: %s' % (database))

# Set URL for Database Writes
if '443' in port:
    url = 'https://%s/influx/write?db=%s' % (server,database)
else:
    url = 'http://%s:%s/write?db=%s' % (server,port,database)

# Set JSON Web Token (JWT) from key_store.db
headers = {
    'Content-type': 'application/x-www-form-urlencoded',
    'Authorization': ''
}
if key_store.get('jwt') is None:
    print('JSON Web Token can be blank if InfluxDB does not use authentication') 
    key_store.set('jwt', input('Enter JSON Web Token (JWT) - '))
headers['Authorization'] = 'Bearer %s' % key_store.get('jwt')

# Print some helpful information:
print('ADC Pin Number:  %s' % ADC_PIN)
print('Client ID:       %s' % client_id)
print('InfluxDB Server: %s:%s' % (server,port))
print('Database Name:   %s' % database)
print('Measurement:     %s' % measurement)
print()
print('=' * 45)
print()


def main():

    gc.collect()  # Loop runs device out of memory without this
    # Uncomment to monitor RAM usage
    #print('Free Memory: %sKB' % int(gc.mem_free()/1024)) 

    # Read the eTape Sensor
    water = Milone_eTape.inches()
    #print('Inches of Water: %.01f' % water)

    # Send the Data to Server
    data = "%s,device=%s inches=%.01f" % (measurement, client_id, water)
    print(data)
    response = urequests.post(url,headers=headers,data=data)
    #print('STATUS:', response.status_code)
    if '204' in str(response.status_code):  # HTTP Status 204 (No Content) indicates server successfull fulfilled request with no response content
        print('InfluxDB write: Success')
        print()
        if 'TinyPICO' in uname().machine:
            led.blink(0,255,0,ms=1500,i=1) # Green
    else:
        print('InfluxDB write: Failed')
        if 'TinyPICO' in uname().machine:
            led.solid(255,127,0)  # Orange
        sleep(sleep_interval)
        reset()


while True:
    try:
        main()
        wdt_feed(sleep_interval * 10)  # Keep Watchdog Timer from resetting device for 2x sleep_interval
        sleep(sleep_interval)
    except KeyboardInterrupt:
        wdt_feed(WDT_CANCEL)  # Cancel/Disable Watchdog Timer when Ctrl+C pressed
        exit()
    except:
        sleep(sleep_interval)
        reset()


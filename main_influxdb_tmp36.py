#
# Brandon Gant
# Created: 2020-09-09
#
# Espressif ESP32-PICO-KIT_V4.1 board with ESP32-PICO-D4 chip 
# Analog Devices TMP36
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
#    put main_influxdb_tmp36.py main.py
#    put client_id.py
#    put AnalogDevices_TMP36.py
#
#    repl
#    from machine import reset
#    reset()
#
# InfluxDB query examples:
#    curl -sG "http://influxdb.localdomain:8086/query?pretty=true" --data-urlencode "q=SHOW DATABASES"
#    curl -sG "http://influxdb.localdomain:8086/query?pretty=true" --data-urlencode "db=test" --data-urlencode "q=SHOW MEASUREMENTS"
#    curl -sG "http://influxdb.localdomain:8086/query?pretty=true" --data-urlencode "db=test" --data-urlencode "q=SELECT * FROM garage ORDER BY DESC LIMIT 3"
#       NOTE: If there are '-' and '_' characters in the measurement name change query format to: FROM \"garage-bay\" ORDER
#    curl -sG "http://influxdb.localdomain:8086/query?pretty=true" --data-urlencode "q=DROP DATABASE test"
#

from soft_wdt import wdt_feed, WDT_CANCEL  # Initialize Watchdog Timer
wdt_feed(60)  # main.py script has 1 minute to initialize and loop before Watchdog timer resets device

from machine import reset
from time import sleep
import urequests
import gc 

import key_store
from sys import exit

import AnalogDevices_TMP36

# Get Unique Machine ID
from client_id import client_id
print('Client ID:', client_id)

# Get InfluxDB server:port:database:measurement from key_store.db
# i.e. influxdb.localdomain:8086:test:garage
server,port,database,measurement = key_store.get('influxdb').split(':')

sleep_interval = 30  # Seconds

# Create database if it does not already exist (only works with no authentication or admin rights)
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
    url = 'https://%s/write?db=%s' % (server,database)
else:
    url = 'http://%s:%s/write?db=%s' % (server,port,database)

# Set JSON Web Token (JWT) from key_store.db
headers = {
    'Content-type': 'application/x-www-form-urlencoded',
    'Authorization': ''
}
headers['Authorization'] = 'Bearer %s' % key_store.get('jwt')


print('=' * 45)
print()


def main():

    gc.collect() # Free up Heap space after each loop to avoid urequests memory leak 
    # Uncomment to monitor RAM usage
    #print('Free Memory: %sKB' % int(gc.mem_free()/1024))

    # Read the TMP36 Sensor
    temperature = round(AnalogDevices_TMP36.read_temp(gpio_pin_number=32,scale='F'), 1)
    #print('Fahrenheit: %.01f' % temperature)

    # Send the Data to Server (Try to avoid '-' and '_' characters in InfluxDB Key names)
    data = "%s,clientid=%s temperature=%.01f" % (measurement, client_id, temperature)
    print(data)
    response = urequests.post(url,headers=headers,data=data)
    #print('STATUS:', response.status_code)
    if '204' in str(response.status_code):  # HTTP Status 204 (No Content) indicates server successfull fulfilled request with no response content
        print('InfluxDB write: Success')
        print()
    else:
        print('InfluxDB write: Failed')
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


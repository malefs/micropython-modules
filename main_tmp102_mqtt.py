# SparkFun ESP32 Thing: https://www.sparkfun.com/products/13907
# MicroPython:          https://docs.micropython.org/en/latest/
#
# Brandon Gant
# Created: 2019-03-28
# Updated: 2019-12-20
#
# Usage:
#    ampy -p /dev/ttyUSB0 put main_tmp102.py /main.py
#
# Temperature Logger:
# This script uses a TMP102 sensor to check the temperature every five minutes
# and log the results to an MQTT server as well as locally.
#

import utime
print('main.py: Press CTRL+C to drop to REPL...')
utime.sleep(3)

from machine import reset, deepsleep
import mqtt
import SparkFun_TMP102 as tmp102

# Get Unique Client ID
from ubinascii import hexlify
from machine import unique_id
client_id = hexlify(unique_id()).decode('utf-8')  # String with Unique Client ID

# Get MQTT Broker IP from key_store.db
import btree
f = open('key_store.db', 'r+b')
db = btree.open(f)
broker = db[b'mqtt_broker'].decode('utf-8')
topic = 'devices/' + client_id


def main():
    # Read Timestamp and Data
    timestamp = utime.time()   # Epoch UTC
    temperature = round(tmp102.read_temp('F'), 1)

    # Send Data to MQTT Broker
    mqtt.publish(broker, topic + '/temp/value', str(temperature))

    # Log Timestamp and Data locally?
    log_local(timestamp, temperature)

    t = utime.localtime(timestamp)
    print('{:4d}-{:0>2d}-{:0>2d} {:0>2d}:{:0>2d}:{:0>2d} UTC   {}'.format(t[0], t[1], t[2], t[3], t[4], t[5], temperature))
    utime.sleep(1)  # Give UART time to print text before going to sleep


# Log Timestamp and Data locally
def log_local(timestamp, temperature):
    f = open('key_store.db', 'r+b')
    db = btree.open(f)
    db[str(timestamp)] = str(temperature)
    db.flush()
    db.close()


while True:
    main()
    #deepsleep(300000)
    utime.sleep(30)


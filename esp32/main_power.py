# SparkFun ESP32 Thing: https://www.sparkfun.com/products/13907
# SparkFun Battery:     https://www.sparkfun.com/products/13813
# MicroPython:          https://docs.micropython.org/en/latest/
#
# Brandon Gant
# 2019-03-28
#
# Usage:
#    ampy -p /dev/ttyUSB0 put main_power.py /main.py
#
# Power Outage Dectection:
# The ESP32 gets power from a wall outlet via USB and a battery. A pair
# of 10Kohm resistors is connected from VUSB (5V) to GND. Between the resistors
# a 2.5V wire is connected to an input pin. If house power is lost, VUSB goes to 0.
# A timestamp and power status change are sent to the MQTT server and logged locally.
# For MQTT to work, your WiFi and network must be on a UPS during the power outage.
#

from machine import Pin
import btree
import client
import mqtt
import utime

# 2.5V Input Pin (any GPIO pin should work)
pin = Pin(37, Pin.IN)

# Get Unique Client ID
unique_id = str(client.id())

# Get MQTT Broker IP Address
f = open('key_store.db', 'r+b')
db = btree.open(f)
broker = db[b'mqtt_broker'].decode('utf-8')
db.close()

# Set basename for MQTT Topic
topic = 'devices/' + unique_id

# Initialize variables and assume power is on
current_power_status = 1
last_power_status = 1

print('Monitoring Power...')
while True:
    current_power_status = pin.value()
    if current_power_status != last_power_status:
        # Send power changes to MQTT server
        timestamp = utime.time()
        mqtt.publish(broker, topic + '/power/timestamp', str(timestamp))  # Epoch UTC
        mqtt.publish(broker, topic + '/power/value', str(current_power_status))
        
        # Store power changes locally
        f = open('key_store.db', 'r+b')
        db = btree.open(f)
        db[str(timestamp)] = str(current_power_status) 
        db.flush()
        db.close()

        last_power_status = current_power_status

    utime.sleep(0.5) 


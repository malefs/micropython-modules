# SparkFun ESP32 Thing: https://www.sparkfun.com/products/13907
# MicroPython:          https://docs.micropython.org/en/latest/
# Source Tutorial:
#    https://boneskull.com/micropython-on-esp32-part-2/
#
# Brandon Gant
# Created: 2019-03-17
# Updated: 2019-12-20
#
# Usage:
#    import mqtt
#    mqtt.publish('192.168.1.50', 'test/light', 'off')
#
# This script just provides a modular way to send data to a MQTT server
#

from ubinascii import hexlify
from machine import unique_id
client_id = hexlify(unique_id()).decode('utf-8')  # String with Unique Client ID

from umqtt.simple import MQTTClient

def publish(broker, topic, message):

    mqtt = MQTTClient(client_id, broker)

    try:
        mqtt.connect()
        mqtt.publish(topic, message)
        mqtt.disconnect()
    except:
        print("Connection to MQTT Server %s failed..." % broker)


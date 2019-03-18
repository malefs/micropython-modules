# SparkFun ESP32 Thing: https://www.sparkfun.com/products/13907
# MicroPython:          https://docs.micropython.org/en/latest/
# Source Tutorial:
#    https://boneskull.com/micropython-on-esp32-part-2/
#
# Brandon Gant
# 2019-03-17
#
# Usage:
#    import mqtt
#    mqtt.publish('192.168.1.50', 'test/light', 'off')

from umqtt.simple import MQTTClient
import client

def publish(broker, topic, message):

    mqtt = MQTTClient(client.id(), broker)

    try:
        mqtt.connect()
        mqtt.publish(topic, message)
        mqtt.disconnect()
    except:
        print("Connection to MQTT Server %s failed..." % broker)


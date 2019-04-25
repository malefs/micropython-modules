# SparkFun ESP32 Thing: https://www.sparkfun.com/products/13907
# SparkFun Battery:     https://www.sparkfun.com/products/13813
# MicroPython:          https://docs.micropython.org/en/latest/
#
# Brandon Gant
# 2019-04-25
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

from sparkfun_esp32_blue_led import blue_led
import key_store
from machine import Pin
from mqtt_as import MQTTClient, config
import uasyncio as asyncio
import utime
import ntptime

# Turn off blue led
blue_led(0)

# 2.5V Input Pin (any GPIO pin should work)
pin = Pin(37, Pin.IN)

# Initialize variables (assume power is currently on)
current_power_status = 1
last_power_status = 1

# Set RTC using NTP
def ntp():
    ntptime.host = key_store.get('ntp_host')
    print("NTP Server:", ntptime.host)
    while utime.time() < 10000:  # Retry until clock is set
        ntptime.settime()
        utime.sleep(1)
    print('UTC Time:   {}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(*utime.localtime()))

async def main(client):
    # Called once on startup
    await client.connect()
    ntp()

    # Main loop that publishes to broker
    global current_power_status
    global last_power_status
    while True:
        current_power_status = pin.value()
        if current_power_status != last_power_status:
            timestamp = str(utime.time())
            print(timestamp, current_power_status)
            key_store.set(timestamp, str(current_power_status))

            # If WiFi is down the following will pause for the duration.
            await client.publish('devices/' + config['client_id'].decode('utf-8') + '/demo/timestamp', timestamp, qos = 1)
            await client.publish('devices/' + config['client_id'].decode('utf-8') + '/demo/value', str(current_power_status), qos = 1)
            last_power_status = current_power_status

# Override default mqtt_as.py config variable settings
config['ssid']    = key_store.get('ssid_name')
config['wifi_pw'] = key_store.get('ssid_pass')
config['server']  = key_store.get('mqtt_broker')

MQTTClient.DEBUG = False  # Optional: print diagnostic messages
client = MQTTClient(config)
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors

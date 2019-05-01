# SparkFun ESP32 Thing: https://www.sparkfun.com/products/13907
# Milone Technologies:  https://milonetech.com/products/standard-etape-assembly
# Micropython:          https://docs.micropython.org/en/latest/esp32/quickref.html#adc-analog-to-digital-conversion
#
# Brandon Gant
# 2019-03-29
#
# Usage:
#    ampy -p /dev/ttyUSB0 put main_etape.py /main.py
#
# Sump Pit Level:
# This script uses a Milone eTape with Volage Divider to monitor the level 
# of water in a home sump pit.
#
# Pinout:
#    Red   --> 3.3V
#    Black --> GND
#    White --> GPIO36  (any ADC pin 32-39 will work)
#

from sparkfun_esp32_blue_led import blue_led
import key_store
import machine
import micropython
from mqtt_as import MQTTClient, config
import uasyncio as asyncio
import utime
import ntptime

# Create exceptions (feedback) in cases where normal RAM allocation fails (e.g. interrupts)
micropython.alloc_emergency_exception_buf(100)

# Set RTC using NTP
async def ntp():
    ntptime.host = key_store.get('ntp_host')
    print("NTP Server:", ntptime.host)
    while utime.time() < 10000:  # Retry until clock is set
        ntptime.settime()
        await asyncio.sleep(1)
    print('UTC Time:   {}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(*utime.localtime()))

# Enable blue_led if Wifi is DISCONNECTED
async def wifi_handler(state):
    blue_led(not state)
    await asyncio.sleep(1)

async def main(client):
    # Called once on startup
    await client.connect()
    #await ntp()

    # any ADC pin 32-39 should work
    adc = machine.ADC(machine.Pin(36))
    adc.atten(machine.ADC.ATTN_11DB)   # 0V to 3.3V range
    adc.width(machine.ADC.WIDTH_10BIT) # 0  to 1023 bits read

    # Turn OFF blue led
    #    ON Full means Wifi is DISCONNECTED
    #    ON Weak means device has crashed
    blue_led(0)

    # Main loop that publishes to broker
    print("Monitoring water level...")
    while True:
        await asyncio.sleep(2)
        current_water_level = adc.read()
        timestamp = str(utime.time())
        #key_store.set(timestamp, str(current_power_status))

        # If WiFi is down the following will pause for the duration.
        #await client.publish('devices/' + config['client_id'].decode('utf-8') + '/water/timestamp', timestamp, qos = 1)
        await client.publish('devices/' + config['client_id'].decode('utf-8') + '/water/value', str(current_water_level), qos = 1)

# Override default mqtt_as.py config variable settings
config['wifi_coro'] = wifi_handler
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

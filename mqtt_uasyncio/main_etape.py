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

# Manual measurements of etape ADC values at half-inch increments
def conversion(raw_adc):
    if       raw_adc >= 569 and raw_adc < 583: inches = 8.5   # Normal summer water level
    elif     raw_adc >= 563 and raw_adc < 569: inches = 8.0   # 
    elif     raw_adc >= 583 and raw_adc < 589: inches = 9.0   # Main Sump switches  on at about 585
    elif     raw_adc >= 498 and raw_adc < 563:                # Main Sump switches off at 498 and fills with water
        if   raw_adc >= 498 and raw_adc < 502: inches = 4.0
        elif raw_adc >= 502 and raw_adc < 512: inches = 4.5
        elif raw_adc >= 512 and raw_adc < 520: inches = 5.0
        elif raw_adc >= 520 and raw_adc < 526: inches = 5.5
        elif raw_adc >= 526 and raw_adc < 538: inches = 6.0
        elif raw_adc >= 538 and raw_adc < 545: inches = 6.5
        elif raw_adc >= 545 and raw_adc < 552: inches = 7.0
        elif raw_adc >= 552 and raw_adc < 563: inches = 7.5
    elif raw_adc < 498:                                       # Dry sump pit
        if   raw_adc >=   0 and raw_adc < 455: inches = 1.0
        elif raw_adc >= 455 and raw_adc < 465: inches = 1.5
        elif raw_adc >= 465 and raw_adc < 475: inches = 2.0
        elif raw_adc >= 475 and raw_adc < 480: inches = 2.5
        elif raw_adc >= 480 and raw_adc < 490: inches = 3.0
        elif raw_adc >= 490 and raw_adc < 498: inches = 3.5
    elif raw_adc >= 589:                                      # Main Sump Failure
        if   raw_adc >= 589 and raw_adc < 598: inches = 9.5
        elif raw_adc >= 598 and raw_adc < 610: inches = 10.0
        elif raw_adc >= 610 and raw_adc < 618: inches = 10.5
        elif raw_adc >= 618 and raw_adc < 632: inches = 11.0
        elif raw_adc >= 632 and raw_adc < 644: inches = 11.5
        elif raw_adc >= 644 and raw_adc < 655: inches = 12.0
        elif raw_adc >= 655 and raw_adc < 666: inches = 12.5
        elif raw_adc >= 666 and raw_adc < 679: inches = 13.0
        elif raw_adc >= 679 and raw_adc < 692: inches = 13.5
        elif raw_adc >= 692 and raw_adc < 700: inches = 14.0
        elif raw_adc >= 700 and raw_adc < 711: inches = 14.5
        elif raw_adc >= 711 and raw_adc < 729: inches = 15.0
        elif raw_adc >= 729 and raw_adc < 741: inches = 15.5
        elif raw_adc >= 741 and raw_adc < 780: inches = 16.0
        elif raw_adc >= 780 and raw_adc < 804: inches = 16.5
        elif raw_adc >= 804 and raw_adc < 812: inches = 17.0
        elif raw_adc >= 812 and raw_adc < 830: inches = 17.5
        elif raw_adc >= 830:                   inches = 18.0
    else:
        inches = "error"

    # bottom of etape is one inch above the base of the sump pit
    inches += 1
    return inches

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
        timestamp = str(utime.time())
        current_raw_adc = adc.read()
        current_inches  = conversion(current_raw_adc)
        #key_store.set(timestamp, str(current_water_level))

        # If WiFi is down the following will pause for the duration.
        #await client.publish('devices/' + config['client_id'].decode('utf-8') + '/water/timestamp', timestamp, qos = 1)
        await client.publish('devices/' + config['client_id'].decode('utf-8') + '/water/raw_adc', str(current_raw_adc), qos = 1)
        await client.publish('devices/' + config['client_id'].decode('utf-8') + '/water/inches',  str(current_inches),  qos = 1)

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

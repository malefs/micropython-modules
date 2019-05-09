# SparkFun ESP32 Thing: https://www.sparkfun.com/products/13907
# Milone Technologies:  https://milonetech.com/products/standard-etape-assembly
# Micropython:          https://docs.micropython.org/en/latest/esp32/quickref.html#adc-analog-to-digital-conversion
#
# Brandon Gant
# 2019-03-29
#
# Usage:
#    ampy -p /dev/ttyUSB0 put main_eTape.py /main.py
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

import machine
import utime

adc = machine.ADC(machine.Pin(36))
adc.atten(machine.ADC.ATTN_11DB)   # 0V to 3.3V range
adc.width(machine.ADC.WIDTH_12BIT) # 0  to 4095 bits read

while True:
    adc.read()
    utime.sleep(1)


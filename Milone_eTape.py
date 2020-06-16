# Milone Technologies:  https://milonetech.com/products/standard-etape-assembly
# Micropython:          https://docs.micropython.org/en/latest/esp32/quickref.html#adc-analog-to-digital-conversion
#
# Brandon Gant
# 2020-06-08
#
# Sump Pit Level:
# This script uses a Milone eTape with Volage Divider to monitor the level 
# of water in a home sump pit.
#
# Pinout:
#    Red   --> 3.3V
#    Black --> GND
#    White --> GPIO32  (any ADC pin 32-39 should work)
#

from time import sleep 
from machine import Pin, ADC
adc = ADC(Pin(32))
adc.atten(ADC.ATTN_11DB)   # 0V to 3.3V range
adc.width(ADC.WIDTH_10BIT) # 0  to 1023 bits read


# Single reading from eTape
def read():
    return adc.read()


# Instead of a single reading let's take the average of multiple readings
def average():
    adc_sample = []
    for x in range(22):
        adc_sample.append(adc.read())
        sleep(0.01)
    remove_high_low = sorted(adc_sample)[2:-2]
    average_adc = sum(remove_high_low) / len(remove_high_low)
    return round(average_adc)


# Re-maps a number from one range to another.
# Python equivalent to Arduino map() function.
# Source: https://www.arduino.cc/reference/en/language/functions/math/map/
def range_map(x, in_min, in_max, out_min, out_max):
    return (x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min


def inches(in_min=480, in_max=620):
    # Based on manual measurements of etape ADC values at half-inch increments
    # Min ADC 480 is  1.5 inches or less (1.0 and less is 472)
    # Max ADC 620 is 10.0 inches
    #
    # Sump switches  ON at about 585
    # Sump switches OFF at about 500 and fills with water

    out_min = 1.5
    out_max = 10.0
    inches = range_map(average(), in_min, in_max, out_min, out_max)

    # bottom of etape is about one inch above the base of the sump pit
    #inches += 1

    return round(inches, 1)


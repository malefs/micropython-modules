#
# Brandon Gant
# 2019-12-18
#

from sys import exit
from machine import ADC
from uos import uname
from time import sleep

def read_adc(gpio_pin_number=37):
    # Find Temperature just using the math equations (appears to be off)
    from machine import Pin
    adc = ADC(Pin(gpio_pin_number)) # Pins 32-39 are valid
    adc.atten(ADC.ATTN_6DB)         # 0-2V
    adc.width(ADC.WIDTH_12BIT)      # 0-4095 values

    # Instead of a single reading let's take the average of multiple readings
    adc_sample = []
    for x in range(50):
        adc_sample.append(adc.read())
        sleep(0.01)
    remove_high_low = sorted(adc_sample)[10:-10]
    average_adc = sum(remove_high_low) / len(remove_high_low)

    millivolts = average_adc * (2000/4095)  # Example: 750mV = 1535.6 * (2000/4095)
    temp_celsius = (millivolts - 500) / 10  # Example: 25C = (750mV - 500) / 10
    temp_fahrenheit = (temp_celsius * 9/5) + 32

    return average_adc, millivolts, temp_celsius, temp_fahrenheit


def read_temp(gpio_pin_number, scale='c', in_min=205, in_max=3495):
    hardware = uname().sysname
    if 'esp32' in hardware:
        # Source: https://docs.micropython.org/en/latest/esp32/quickref.html#adc-analog-to-digital-conversion
        from machine import Pin
        adc = ADC(Pin(gpio_pin_number))  # Pins 32-39 are valid
        adc.atten(ADC.ATTN_6DB)          # 0-2V (TMP36 max output voltage is 1.75V)
        adc.width(ADC.WIDTH_12BIT)       # 0-4095 values

        # TMP36 Voltage to ADC scale
        # Min  100mV at -40C is ADC  205
        # Max 1750mV at 125C is ADC 3583 / Using lower value to calibrate with TMP102 and La Crosse readings
        #      750mV at  25C is ADC 1536

        # TMP36 Temperature scale
        if scale.lower() is 'c': 
            out_min = -40  # Minimum Celsius value
            out_max = 125  # Maximum Celsius value
        elif scale.lower() is 'f':  # (Celsius * 9/5) + 32
            out_min = -40  # Minimum Fahrenheit value 
            out_max = 257  # Maximum Fahrenheit value
        else:
            print('unknown temperature scale')
            exit(1)

        # Instead of a single reading let's take the average of multiple readings
        adc_sample = []
        for x in range(50):
            adc_sample.append(adc.read())
            sleep(0.01)
        remove_high_low = sorted(adc_sample)[10:-10]
        average_adc = sum(remove_high_low) / len(remove_high_low)
        average_temp = range_map(average_adc, in_min, in_max, out_min, out_max)
        average_temp = round(average_temp, 1)
       
        return average_temp


    elif 'esp8266' in hardware:
        # I am using the range_map() function below with measured datapoints:
        #   ADC 217 is 750mV at 25C/77F
        #   ADC 162 is 558mV at  7C/44F
        #   ADC 132 is 455mV at -4C/27F

        adc = ADC(0)  # gpio_pin_number is ignored since there is only one ADC on ESP8266
        temp = adc.read()  # ADC value from 0 to 1023
        if scale.lower() is 'f':
            temp = range_map(temp, 132, 217, 27, 77)  # ADC Conversion to Fahrenheit
        elif scale.lower() is 'c':
            temp = range_map(temp, 132, 217, -4, 25)  # ADC Conversion to Celsius
        else:
            print('unknown temperature scale')
            exit(1)
        temp = round(temp, 1)  # Rounding to one decimal place
        return temp            # Return Temperature


    else:
        print('unknown hardware')


# Re-maps a number from one range to another.
# Python equivalent to Arduino map() function.
# Source: https://www.arduino.cc/reference/en/language/functions/math/map/
def range_map(x, in_min, in_max, out_min, out_max):
    return (x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min


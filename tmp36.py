#
# Brandon Gant
# 2019-12-18
#

from sys import exit
from machine import ADC
from uos import uname

def read_temp(gpio_pin_number, scale='c'):
    hardware = uname().sysname
    if 'esp32' in hardware:
        # Source: https://docs.micropython.org/en/latest/esp32/quickref.html#adc-analog-to-digital-conversion
        from machine import Pin
        adc = ADC(Pin(gpio_pin_number))  # Pins 32-39 are valid
        adc.atten(ADC.ATTN_6DB)          # 0-2V (TMP36 max output voltage is 1.75V)
        adc.width(ADC.WIDTH_12BIT)       # 0-4095 values

        # TMP36 Voltage to ADC scale
        in_min = 205   # Min  100mV at -40C is ADC  205
        in_max = 3453  # Max 1750mV at 125C is ADC 3583 but using 3453 to calibrate with TMP102 readings
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

        return round(range_map(adc.read(), in_min, in_max, out_min, out_max), 1) 

    elif 'esp8266' in hardware:
        # I am using the range_map() function below with measured datapoints:
        #   ADC 217 is 750mV at 25C/77F
        #   ADC 162 is 558mV at  7C/44F
        #   ADC 132 is 455mV at -4C/27F

        adc = ADC(0)
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


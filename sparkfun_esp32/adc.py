# Source: https://learn.sparkfun.com/tutorials/micropython-programming-tutorial-getting-started-with-the-esp32-thing/experiment-3-analog-input

import machine
import sys
import utime

# Pin Definitions
repl_button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
repl_led = machine.Pin(5, machine.Pin.OUT)
adc_pin = machine.Pin(36)

# Create an ADC object out of our pin object
adc = machine.ADC(adc_pin)

# 11dB attenuation means full 0V to 3.3V range
adc.atten(adc.ATTN_11DB)

# Blink forever
while True:

    # If button 0 is pressed, drop to REPL
    if repl_button.value() == 0:
        print("Dropping to REPL")
        repl_led.value(1)
        sys.exit()

    # Read ADC and convert to voltage
    val = adc.read() # Will be a value between 0 and 4095
    val = val * (3.3 / 4095) # Convert to value between 0 and 3.3
    val = round(val, 2)
    print("{:.2f}".format(val) + "V")
 
    # Wait a bit before taking another reading
    utime.sleep_ms(200)

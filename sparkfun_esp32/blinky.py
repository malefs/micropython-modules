# Source: https://learn.sparkfun.com/tutorials/micropython-programming-tutorial-getting-started-with-the-esp32-thing/experiment-1-digital-input-and-output

import machine
import sys
import utime

# Pin definitions
repl_button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
led = machine.Pin(5, machine.Pin.OUT)

# Blink forever
while True:

    # If button 0 is pressed, drop to REPL
    if repl_button.value() == 0:
        print("Dropping to REPL")
        sys.exit()

    # Turn LED on and then off
    led.value(1)
    utime.sleep_ms(500)
    led.value(0)
    utime.sleep_ms(500)   

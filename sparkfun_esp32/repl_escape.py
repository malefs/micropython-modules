# ESP32 running MicroPython module repl_escape.py
# Stop looping main.py by pressing onboard switch 0
#
# Brandon Gant
# 2019-02-08
#
# Source: https://learn.sparkfun.com/tutorials/micropython-programming-tutorial-getting-started-with-the-esp32-thing/experiment-3-analog-input
#

import machine
import sys

# Pin definitions
repl_button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
repl_led = machine.Pin(5, machine.Pin.OUT)

def repl_escape():
    # If button 0 is pressed, drop to REPL
    if repl_button.value() == 0:
        print("Dropping to REPL")
        repl_led.value(1)
        sys.exit()


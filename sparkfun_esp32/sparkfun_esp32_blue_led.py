#
# Usage:
#   from sparkfun_esp32_blue_led import blue_led
#   blue_led(1)
#   blue_led(0)

from machine import Pin
blue_led = Pin(5, Pin.OUT)

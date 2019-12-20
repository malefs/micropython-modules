#
# Usage:
#   from SparkFun_ESP32_Thing_BlueLED import blue_led
#   blue_led(1) or blue_led(True)
#   blue_led(0) or blue_led(False)

from machine import Pin
blue_led = Pin(5, Pin.OUT)

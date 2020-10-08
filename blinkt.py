# Brandon Gant
# Created: 2020-10-07
#
# Wiring: 
#    Blinkt  4  <-->  ESP32 5V
#    Blinkt  6  <-->  ESP32 GND
#    Blinkt 16  <-->  ESP32 SPI MOSI (Data)
#    Blinkt 18  <-->  ESP32 SPI SCK (Clock)
#
# MicroPython Configuration:
#    put micropython_dotstar.py
#    put blinkt.py
#    put <Blinkt script wrritten for Raspberry Pi>.py
#
# Usage:
#    import <Blinkt script written for Raspberry Pi> 
#
# Sources: 
#    https://github.com/mattytrentini/micropython-dotstar
#    https://pinout.xyz/pinout/blinkt
#    https://randomnerdtutorials.com/esp32-pinout-reference-gpios/
#

from micropython_dotstar import DotStar
from machine import SPI,Pin,reset

spi = SPI(sck=Pin(18), mosi=Pin(23), miso=Pin(19))  # Pin 19 is not used or wired
dotstar = DotStar(spi, 8)  # 8 LED's to Control (0 thru 7)

def clear():
    dotstar.fill((0,0,0))

def show():
    dotstar.show()

def set_pixel(led,red,green,blue,brightness=0.5):
    dotstar[led] = (red,green,blue,brightness)

def set_brightness(brightness):
    dotstar.brightness = brightness  # 0.1 to 1.0

def set_clear_on_exit():
    # Not sure what to do with this command
    return


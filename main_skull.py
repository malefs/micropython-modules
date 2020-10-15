
import blinkt
from time import sleep
from machine import reset
from random import randint

print("Press Ctrl+C to stop script...")


def silence(seconds):
    blinkt.clear()  # Clear LED's
    sleep(seconds)


def eyes_forward(seconds):
    blinkt.clear()
    blinkt.set_brightness(0.1)

    # Forward
    blinkt.set_pixel(1,0,255,0)
    blinkt.set_pixel(6,0,255,0)
    sleep(seconds)
    blinkt.clear()
    sleep(0.2)
  
def eyes_left(seconds):
    blinkt.clear()
    blinkt.set_brightness(0.1)

    # Left
    blinkt.set_pixel(0,0,255,0)
    blinkt.set_pixel(5,0,255,0)
    sleep(seconds)
    blinkt.clear()
    sleep(0.2)
    

def eyes_right(seconds):
    blinkt.clear()
    blinkt.set_brightness(0.1)

    # Right
    blinkt.set_pixel(2,0,255,0)
    blinkt.set_pixel(7,0,255,0)
    sleep(seconds)
    blinkt.clear()
    sleep(0.2)


def eyes_looking(cycles):
    eyes_forward(3)
    eyes_forward(3)
    eyes_left(2)
    eyes_right(2)
    eyes_forward(4)
 

def larson_scanner(cycles):
    blinkt.clear()  # Clear LED's
    blinkt.set_brightness(0.1)
    loops = 1

    # The idea is that the leading LED is at 100%, the next at 75%, 50%, etc. 
    # They then follow each other across the LED bar
    i = {0:0, 25:1, 50:2, 75:3, 100:4}          # Initialize Starting Brightness
    direction = {0:1, 25:1, 50:1, 75:1, 100:1}  # Initialize Starting Direction

    while loops < cycles:
        for n in (0,25,50,75,100): # For each brightness level
            if i[n] == 7:  # Upper Bound LED
                direction[n] = -1  # Reverse direction
            if i[n] == 0:  # Lower Bound LED
                direction[n] =  1  # Forward direction
            i[n] = i[n] + direction[n]
    
        #print(i[0], i[25], i[50], i[75], i[100])
        blinkt.set_pixel(i[0],   100, 0, 0, 0.00) # Trailing LED's will stay at low Brightness
        blinkt.set_pixel(i[25],  100, 0, 0, 0.05) # Adjust brightness of each pixel to get a clean look
        blinkt.set_pixel(i[50],  100, 0, 0, 0.10)
        blinkt.set_pixel(i[75],  100, 0, 0, 0.20)
        blinkt.set_pixel(i[100], 100, 0, 0, 0.30)
        blinkt.show()
        sleep(0.1)
        loops += 1


def police(cycles):
    blinkt.clear()  # Clear LED's
    sleep_interval = 0.05  # Seconds
    blinkt.set_brightness(1)
    loops = 1

    while loops < cycles:
        # Blink Red Three Times
        for x in range(3):
            # Turn lights on
            blinkt.set_pixel(0,255,0,0)
            blinkt.set_pixel(1,255,0,0)
            blinkt.set_pixel(2,255,0,0)
            blinkt.set_pixel(3,255,0,0)
            blinkt.show()
            sleep(sleep_interval)
     
            # Turn lights off
            blinkt.clear()
            blinkt.show()
            sleep(sleep_interval)

        # Blink Blue Three Times
        for x in range(3):
            # Turn lights on
            blinkt.set_pixel(4,0,0,255)
            blinkt.set_pixel(5,0,0,255)
            blinkt.set_pixel(6,0,0,255)
            blinkt.set_pixel(7,0,0,255)
            blinkt.show()
            sleep(sleep_interval)

            # Turn lights off
            blinkt.clear()
            blinkt.show()
            sleep(sleep_interval)

        loops += 1


try:
    while True:
        eyes_looking(30)
        silence(10)
        police(15)
        silence(10)
        larson_scanner(100)
        silence(10)
       

except KeyboardInterrupt:
    blinkt.clear()
    blinkt.show()


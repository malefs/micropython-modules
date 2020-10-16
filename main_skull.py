import blinkt
from time import sleep,ticks_cpu
from machine import reset
import random
import gc

print("Press Ctrl+C to stop script...")

# Random numbers are the same every reset (this appears to fix it)
random.seed(ticks_cpu())
for x in range(0,random.randint(25,75)): random.random()
random.seed(ticks_cpu())

def eyes_forward(seconds,r,g,b):
    blinkt.clear()
    blinkt.set_pixel(1,r,g,b)
    blinkt.set_pixel(6,r,g,b)
    sleep(seconds)
    blinkt.clear()
    sleep(0.2)
  
def eyes_left(seconds,r,g,b):
    blinkt.clear()
    blinkt.set_pixel(0,r,g,b)
    blinkt.set_pixel(5,r,g,b)
    sleep(seconds)
    blinkt.clear()
    sleep(0.2)

def eyes_right(seconds,r,g,b):
    blinkt.clear()
    blinkt.set_pixel(2,r,g,b)
    blinkt.set_pixel(7,r,g,b)
    sleep(seconds)
    blinkt.clear()
    sleep(0.2)

def eyes_looking(cycles):
    blinkt.clear()
    states = (eyes_forward, eyes_left, eyes_right)
    loops = 1

    green  = (0,255,0)
    red    = (255,0,0)
    blue   = (0,0,255)
    purple = (255,0,255)
    teal   = (0,255,255)
    yellow = (255,255,0)
    orange = (255,50,0)
    white  = (255,255,255)
    eye_color = (green, red, blue, purple, orange, yellow)
    r,g,b = random.choice(eye_color)

    blinkt.set_brightness(random.randint(1,10)/100)

    while loops < cycles:    
        random_function = random.choice(states)
        open = random.randint(2,6)
        random_function(open,r,g,b)
        loops += 1
    blinkt.clear()


def larson_scanner(cycles):
    blinkt.clear()
    blinkt.set_brightness(0.5)
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
    blinkt.clear()


def police(cycles):
    blinkt.clear()
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
    blinkt.clear()


try:
    while True:
        gc.collect() 
        weighted_choice = random.randint(0,100)
        if weighted_choice < 90:
            eyes_looking(random.randint(5,10))
        elif weighted_choice < 95:
            police(random.randint(5,10))
        else: 
            larson_scanner(random.randint(50,90))
        sleep(random.randint(5,30))

except KeyboardInterrupt:
    blinkt.clear()


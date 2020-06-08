# Python for Microcontrollers, Page 41

import pyb

# Avoid "magic" numbers
red, green, yellow, blue = range(1,5)

# Interrupt Service Routine (ISR)
def BlinkYellow():

    # If LED on during interrupt, turn off
    pyb.LED(red).off()
    pyb.LED(green).off()
    pyb.LED(blue).off()

    # Blink Yellow LED
    for x in range(0,4):
        pyb.LED(yellow).on()
        pyb.delay(1000)
        pyb.LED(yellow).off()
        pyb.delay(1000)

usr_button = pyb.Switch()
usr_button.callback(BlinkYellow)

# Main Loop
while True:
    pyb.LED(red).on()
    pyb.LED(blue).off()
    pyb.delay(500)
    pyb.LED(red).off()
    pyb.LED(blue).on()
    pyb.delay(500)


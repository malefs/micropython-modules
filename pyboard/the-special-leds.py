# http://docs.micropython.org/en/latest/pyboard/tutorial/leds.html#the-special-leds
#
# Yellow and Blue LED's are special since you can control intensity without PWM

try:
    led = pyb.LED(4)
    intensity = 0
    while True:
        intensity = (intensity + 1) % 255
        led.intensity(intensity)
        pyb.delay(20)

finally:
    led.off()

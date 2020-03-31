# http://docs.micropython.org/en/latest/pyboard/tutorial/accel.html#using-the-accelerometer

accel = pyb.Accel()
light = pyb.LED(3)
SENSITIVITY = 3

while True:
    x = accel.x()
    if abs(x) > SENSITIVITY:
        light.on()
    else:
        light.off()

    pyb.delay(100)

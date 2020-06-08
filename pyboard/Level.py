accel = pyb.Accel()
light = pyb.LED(4)
SENSITIVITY = 3

while True:
    x = accel.x()
    if abs(x) > SENSITIVITY:
        light.on()
    else:
        light.off()

    for i in range(10):
        print(accel.x(), accel.y(), accel.z())

    pyb.delay(500)

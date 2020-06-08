# http://docs.micropython.org/en/latest/pyboard/tutorial/usb_mouse.html#making-a-mouse-with-the-accelerometer
#
# Edit boot.py and uncomment the line: pyb.usb_mode('VCP+HID')

import pyb

switch = pyb.Switch()
accel = pyb.Accel()
hid = pyb.USB_HID()

while not switch():
    hid.send((0, accel.x(), accel.y(), 0))
    pyb.delay(20)

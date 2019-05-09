
# Useful Info for MicroPython on the ESP32

https://micropython.org/download/#esp32

/home/pi/.local/bin/esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash<br>
/home/pi/.local/bin/esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32-20190125-v1.10.bin

/home/pi/.local/bin/ampy --port /dev/ttyUSB0 put tmp102.py<br>
screen /dev/ttyUSB0 115200

Screen Commands:
* Ctrl+a Shift+k - Terminate screen connection
 
REPL Commands:
* Module Documentation:
  * help()  <-- Welcome to MicroPython screen
  * help('modules')  <-- List installed modules
  * import ntptime; help(ntptime)
* List file systems:
  * import sys 
  * sys.path
* List files:
  * import uos
  * uos.listdir('/')


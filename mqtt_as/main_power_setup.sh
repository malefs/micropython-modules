#!/bin/bash

esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
sleep 7
esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 ~/Downloads/esp32-bluetooth.bin 

echo "Waiting 20 seconds for reboot..."
sleep 20

echo "Creating uasyncio directory..."
ampy -p /dev/ttyUSB0 mkdir uasyncio

echo "Loading __init__.py..."
ampy -p /dev/ttyUSB0 put ~/source/micropython-modules/mqtt_as/uasyncio/__init__.py uasyncio/__init__.py

echo "Loading core.py..."
ampy -p /dev/ttyUSB0 put ~/source/micropython-modules/mqtt_as/uasyncio/core.py uasyncio/core.py

echo "Loading mqtt_as.py..."
ampy -p /dev/ttyUSB0 put ~/source/micropython-modules/mqtt_as/mqtt_as.py 

echo "Loading key_store.py..."
ampy -p /dev/ttyUSB0 put ~/source/micropython-modules/key_store.py 

echo "Loading sparkfun_esp32_blue_led.py..."
ampy -p /dev/ttyUSB0 put ~/source/micropython-modules/sparkfun_esp32/sparkfun_esp32_blue_led.py 

echo "Loading main_power.py..."
ampy -p /dev/ttyUSB0 put ~/source/micropython-modules/mqtt_as/main_power.py /main.py

echo "Manually run the following commands to initialize settings:"
echo "   screen /dev/ttyUSB0 115200"
echo "   import key_store"
echo "   key_store.init()"


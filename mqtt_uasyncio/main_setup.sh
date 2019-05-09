#!/bin/bash

if [ $1 == "erase" ]
then
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
sleep 1
esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 ~/Downloads/esp32-bluetooth.bin 
fi

if [ $1 == "ampy" ]
then
AMPY="ampy --port /dev/ttyUSB0 --baud 115200 --delay 1"

echo "Creating uasyncio directory..."
ampy -p /dev/ttyUSB0 mkdir uasyncio

echo "Loading __init__.py..."
$AMPY put ~/source/micropython-lib/uasyncio/uasyncio/__init__.py uasyncio/__init__.py

echo "Loading core.py..."
$AMPY put ~/source/micropython-lib/uasyncio.core/uasyncio/core.py uasyncio/core.py

echo "Loading mqtt_as.py..."
$AMPY put ~/source/micropython-mqtt/mqtt_as/mqtt_as.py 

echo "Loading key_store.py..."
$AMPY put ~/source/micropython-modules/key_store.py 

echo "Loading sparkfun_esp32_blue_led.py..."
$AMPY put ~/source/micropython-modules/sparkfun_esp32/sparkfun_esp32_blue_led.py 

#echo "Loading main_power.py..."
#$AMPY put ~/source/micropython-modules/mqtt_as/main_power.py /main.py

echo "Manually run the following commands to initialize settings:"
echo "   screen /dev/ttyUSB0 115200"
echo "   import key_store"
echo "   key_store.init()"
echo ""
echo "Manually add your own main.py file"
fi

To use Peter Hinch's mqtt_as.py module you need to copy over the following files:

```
cd ~/source/

git clone https://github.com/peterhinch/micropython-mqtt
ampy -p /dev/ttyUSB0 put ~/source/micropython-mqtt/mqtt_as/mqtt_as.py

git clone https://github.com/micropython/micropython-lib
ampy -p /dev/ttyUSB0 mkdir uasyncio
ampy -p /dev/ttyUSB0 put ~/source/micropython-lib/uasyncio/uasycio/__init__.py /uasyncio/__init__.py
ampy -p /dev/ttyUSB0 put ~/source/micropython-lib/uasyncio.core/uasyncio/core.py /uasyncio/core.py
```

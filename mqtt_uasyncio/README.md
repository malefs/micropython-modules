
```
cd ~/source/
git clone https://github.com/peterhinch/micropython-mqtt
ln -s ~/source/micropython-mqtt/mqtt_as/mqtt_as.py .

git clone https://github.com/micropython/micropython-lib
mkdir uasyncio
ln -s ~/source/micropython-lib/uasyncio/uasyncio/__init__.py uasyncio/
ln -s ~/source/micropython-lib/uasyncio.core/uasyncio/core.py uasyncio/

ampy -p /dev/ttyUSB0 put mqtt_as.py
ampy -p /dev/ttyUSB0 mkdir uasyncio
ampy -p /dev/ttyUSB0 put __init__.py /uasyncio/__init__.py
ampy -p /dev/ttyUSB0 put core.py /uasyncio/core.py
```

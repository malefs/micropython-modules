# SparkFun ESP32 Thing: https://www.sparkfun.com/products/13907
# MicroPython:          https://docs.micropython.org/en/latest/
#
# Brandon Gant
# 2019-02-08
#
# Source: https://github.com/micropython/micropython/tree/master/ports/esp32#configuring-the-wifi-and-using-the-board
# Source: https://boneskull.com/micropython-on-esp32-part-1/
# Source: https://docs.micropython.org/en/latest/library/network.WLAN.html
#
# Usage:
#     /home/pi/.local/bin/ampy --port /dev/ttyUSB0 put boot.py
#     screen /dev/ttyUSB0 115200
#         (Ctrl+a Shift+k to kill screen connection)
#

import utime
print('boot.py: Press CTRL+C to drop to REPL...')
utime.sleep(3)

import btree
import esp
import key_store
import machine
import micropython
import network
import ntptime
import uos
from time import sleep

# Create exceptions (feedback) in cases where normal RAM allocation fails (e.g. interrupts)
micropython.alloc_emergency_exception_buf(100)

ssid_name = key_store.get('ssid_name')
ssid_pass = key_store.get('ssid_pass')

# Connect to WiFI
def wlan_connect(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    counter = 0
    if not wlan.active() or not wlan.isconnected():
        wlan.active(True)
        print('WiFi SSID: ', ssid)
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            counter += 1
            if counter > 60:
                machine.reset()
            sleep(1)
            pass
    print('WiFi DHCP: ', wlan.ifconfig()[0])

# Set RTC using NTP
def ntp():
    print('')
    ntptime.host = key_store.get('ntp_host')
    print("NTP Server:", ntptime.host)
    while utime.time() < 10000:  # Retry until clock is set
        ntptime.settime()
        utime.sleep(1)
    print('UTC Time:   {}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(*utime.localtime()))
    print('')
         

# Suppress ESP debug messages in the REPL
def no_debug():
    esp.osdebug(None)

no_debug()
wlan_connect(ssid_name, ssid_pass)
#ntp()

print("List of files on this device:")
print('   %s' % '\n   '.join(map(str, sorted(uos.listdir('/')))))
print('')

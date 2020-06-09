# MicroPython: https://docs.micropython.org/en/latest/
#
# Brandon Gant
# Created: 2019-02-08
# Updated: 2020-02-14
#
# Source: https://github.com/micropython/micropython/tree/master/ports/esp32#configuring-the-wifi-and-using-the-board
# Source: https://boneskull.com/micropython-on-esp32-part-1/
# Source: https://docs.micropython.org/en/latest/library/network.WLAN.html
#
# Files required to run this script:
#     boot.py (boot_with_wifi.py)
#     key_store.py
#     soft_wdt.py
#
# Usage:
#     $ pip3 install --user mpfshell
#     $ mpfshell
#     mpfs [/]> open ttyUSB0
#     mpfs [/]> put boot_with_wifi.py boot.py
#     mpfs [/]> put key_store.py
#     mpfs [/]> repl
#     >>>  <Ctrl+] to exit repl>
#
# --OR--
#
#     $ ampy --port /dev/ttyUSB0 put boot_with_wifi.py boot.py
#     $ screen /dev/ttyUSB0 115200
#     >>>  <Ctrl+a then Shift+k to exit repl>
#

from soft_wdt import wdt_feed, WDT_CANCEL  # Initialize Watchdog Timer
wdt_feed(120)  # boot.py script has 2 minutes to complete before Watchdog timer resets device

from machine import reset
import utime
print()

print('=' * 45)
print('boot.py: Press CTRL+C to drop to REPL...')
print()
utime.sleep(3)

# Garbage Collection in the default esp8266 boot.py
from uos import uname
if 'esp8266' in uname().sysname:
    from gc import collect
    collect()

# Create exceptions (feedback) in cases where normal RAM allocation fails (e.g. interrupts)
from micropython import alloc_emergency_exception_buf
alloc_emergency_exception_buf(100)

# Load secrets from local key_store.db
try:
    import key_store
    ssid_name = key_store.get('ssid_name')
    ssid_pass = key_store.get('ssid_pass')
except:
    key_store.init()
    reset()

# Connect to WiFI
def wlan_connect(ssid, password):
    import network
    wlan = network.WLAN(network.STA_IF)
    if not wlan.active() or not wlan.isconnected():
        wlan.active(True)
        print('WiFi SSID: ', ssid)
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            utime.sleep(1)
    print('WiFi DHCP: ', wlan.ifconfig()[0])
    print()

# Set RTC using NTP
def ntp():
    import ntptime
    ntptime.host = key_store.get('ntp_host')
    print("NTP Server:", ntptime.host)
    while utime.time() < 10000:  # Retry until clock is set
        ntptime.settime()
        utime.sleep(2)
    print('UTC Time:   {}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(*utime.localtime()))
    print()
         
# Suppress ESP debug messages in the REPL
def no_debug():
    from esp import osdebug
    osdebug(None)

def mem_stats():
    from esp import flash_size
    from uos import statvfs
    fs_stat = statvfs('/')
    fs_size = fs_stat[0] * fs_stat[2]
    fs_free = fs_stat[0] * fs_stat[3]
    print('Storage Information:')
    print('   Flash Size   {:5,}KB'.format(flash_size()/1024))
    print('   File System  {:5,}KB'.format(fs_size/1024))
    print('   Free Space   {:5,}KB'.format(fs_free/1024))
    print()

def list_files():
    print("List of files on this device:")
    print('   %s' % '\n   '.join(map(str, sorted(uos.listdir('/')))))
    print()

# Run selected functions at boot
no_debug()
wlan_connect(ssid_name, ssid_pass)
#ntp()
mem_stats()
list_files()

print('boot.py: end of script')
print('=' * 45)
print()

# Disable boot.py watchdog timer
wdt_feed(WDT_CANCEL)

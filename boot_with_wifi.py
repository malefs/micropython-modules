# MicroPython: https://docs.micropython.org/en/latest/
#
# Brandon Gant
# Created: 2019-02-08
# Updated: 2021-02-01
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
# Optional files:
#     TinyPICO_RGB.py
#     detect_filesystem.py
#
# Usage:
#     $ pip3 install --user mpfshell
#     $ mpfshell
#     mpfs [/]> open ttyUSB0
#     mpfs [/]> put boot_with_wifi.py boot.py
#     mpfs [/]> put key_store.py
#     mpfs [/]> put soft_wdt.py
#     mpfs [/]> put detect_filesystem.py
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
from uos import uname

if 'TinyPICO' in uname().machine:
    import TinyPICO_RGB as led
    led.off()

print()
print('=' * 45)
print('boot.py: Press CTRL+C to drop to REPL...')
print()
utime.sleep(3)  # A chance to hit Ctrl+C in REPL

# Create exceptions (feedback) in cases where normal RAM allocation fails (e.g. interrupts)
from micropython import alloc_emergency_exception_buf
alloc_emergency_exception_buf(100)

# Load secrets from local key_store.db
try:
    import key_store
    ssid_name = key_store.get('ssid_name')
    ssid_pass = key_store.get('ssid_pass')
except:
    wdt_feed(WDT_CANCEL)
    key_store.init()
    reset()

# Connect to WiFI
def wlan_connect(ssid, password):
    import network
    from ubinascii import hexlify
    wlan = network.WLAN(network.STA_IF)
    if not wlan.active() or not wlan.isconnected():
        wlan.active(True)
        print('       MAC: ', hexlify(wlan.config('mac'),':').decode())
        print(' WiFi SSID: ', ssid)
        wlan.connect(ssid, password)
        if 'TinyPICO' in uname().machine:
            led.solid(255,0,255)  # Purple
        start_wifi = utime.ticks_ms()
        while not wlan.isconnected():
            if utime.ticks_diff(utime.ticks_ms(), start_wifi) > 20000:  # 20 second timeout
                print('Wifi Timeout... Resetting Device')
                reset()
    print('        IP: ', wlan.ifconfig()[0])
    print('    Subnet: ', wlan.ifconfig()[1])
    print('   Gateway: ', wlan.ifconfig()[2])
    print('       DNS: ', wlan.ifconfig()[3])
    if 'TinyPICO' in uname().machine:
        led.solid(0,0,255)  # Blue
    print()

# Set RTC using NTP
def ntp():
    import ntptime
    ntptime.host = key_store.get('ntp_host')
    print("NTP Server:", ntptime.host)
    start_ntp = utime.ticks_ms()
    while utime.time() < 10000:  # Clock is not set with NTP if unixtime is less than 10000
        ntptime.settime()
        if utime.ticks_diff(utime.ticks_ms(), start_ntp) > 10000:  # 10 second timeout
                print('NTP Timeout... Resetting Device')
                reset()
    print('  UTC Time: {}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(*utime.localtime()))
    print()
         
# Suppress ESP debug messages in the REPL
def no_debug():
    from esp import osdebug
    osdebug(None)

def mem_stats():
    from esp import flash_size
    from uos import statvfs
    import gc
    fs_stat = statvfs('/')
    fs_size = fs_stat[0] * fs_stat[2]
    fs_free = fs_stat[0] * fs_stat[3]
    print('Memory Information:')
    print('   RAM Size     {:5,}KB'.format(int((gc.mem_alloc() + gc.mem_free())/1024)))
    print()
    print('Flash Storage Information:')
    print('   Flash Size   {:5,}KB'.format(int(flash_size()/1024)))
    print('   File System  {:5,}KB'.format(int(fs_size/1024)))
    print('   Free Space   {:5,}KB'.format(int(fs_free/1024)))
    print()

def filesystem():
    from detect_filesystem import check
    print('File System format:', check())
    print()

def list_files():
    from uos import listdir
    print("List of files on this device:")
    print('   %s' % '\n   '.join(map(str, sorted(listdir('/')))))
    print()

# Run selected functions at boot
try:
    no_debug()
    wlan_connect(ssid_name, ssid_pass)
    ntp()          # Only needed if using HTTPS or local timestamp data logging 
    mem_stats()
    filesystem()
    list_files()
except:
    print('ERROR... Resetting Device')
    if 'TinyPICO' in uname().machine:
        led.solid(255,0,0)  # Red
    utime.sleep(3)  # A chance to hit Ctrl+C in REPL
    reset()

print('boot.py: end of script')
print('=' * 45)
print()

# Disable boot.py watchdog timer
wdt_feed(WDT_CANCEL)

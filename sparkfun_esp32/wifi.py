# Source: https://learn.sparkfun.com/tutorials/micropython-programming-tutorial-getting-started-with-the-esp32-thing/experiment-5-wifi

import machine
import sys
import network
import utime
import urequests

# Pin definitions
repl_button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
repl_led = machine.Pin(5, machine.Pin.OUT)

# Network settings
wifi_ssid = "milton"
wifi_password = "abc11958ff"

# Web page (non-SSL) to get
url = "http://example.com"

# Create a station object to store our connection
station = network.WLAN(network.STA_IF)
station.active(True)

# Continually try to connect to WiFi access point
while not station.isconnected():

    # Try to connect to WiFi access point
    print("Connecting...")
    station.connect(wifi_ssid, wifi_password)

    # Check to see if our REPL button is pressed over 10 seconds
    for i in range(100):
        if repl_button.value() == 0:
            print("Dropping to REPL")
            repl_led.value(1)
            sys.exit()
        utime.sleep_ms(100)

# Continually print out HTML from web page as long as we have a connection
while station.isconnected():

    # Display connection details
    print("Connected!")
    print("My IP Address:", station.ifconfig()[0])

    # Perform HTTP GET request on a non-SSL web
    response = urequests.get(url)

    # Display the contents of the page
    print(response.text)

    # Check to see if our REPL button is pressed over 10 seconds
    for i in range(100):
        if repl_button.value() == 0:
            print("Dropping to REPL")
            repl_led.value(1)
            sys.exit()
        utime.sleep_ms(100)

# If we lose connection, repeat this main.py and retry for a connection
print("Connection lost. Trying again...")


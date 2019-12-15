#
# Brandon Gant
# 2019-12-13
#
# ESP8266 Espressif DevKitC board (ESP-WROOM-02D chip)
# TMP36 temperature sensor with Vout connected to ESP8266 pin ADC (TOUT)
#
# Source: https://github.com/micropython/micropython/blob/master/examples/network/http_client_ssl.py

import usocket as socket
import ussl as ssl
import key_store
from machine import ADC
from time import sleep

# Get ThingSpeak API Key
import btree
f = open('key_store.db', 'r+b')
db = btree.open(f)
thingspeak_api_key = db[b'thingspeak_api_key'].decode('utf-8')
db.close()

server = 'api.thingspeak.com'

def main():
    print('=============================================')
    print()

    # Read the Temperature
    tempf = read_temp()
    print('Temperature Reading: %sF' % tempf)

    # Create the HTTPS GET Request string
    get_request = 'GET /update?api_key=' + thingspeak_api_key + '&field1=' + tempf + ' HTTP/1.0\r\n\r\n'
    get_request = str.encode(get_request)  # Convert Type str to bytes

    # Send the Data to ThingSpeak
    print('Server Connection:', server)
    status = send_data(server, get_request)

    if status:
        print('Status: Success')
    else:
        print('Status: Failed')
    print()


def read_temp():
    # I am using the range_map() function below with measured datapoints:
    #   ADC 217 is 750mV at 25C/77F
    #   ADC 162 is 558mV at  7C/44F
    #   ADC 132 is 455mV at -4C/27F

    adc = ADC(0)
    temp = adc.read()      # ADC value from 0 to 1023
    temp = range_map(temp, 132, 217, 27, 77)  # Conversion to Fahrenheit
    temp = round(temp, 1)  # Rounding to one decimal place
    temp = str(temp)       # Convert to string to put into URL field1
    return temp            # Return Temperature in Fahrenheit


def send_data(server, get_request, use_stream=True):
    s = socket.socket()

    ai = socket.getaddrinfo(server, 443)
    #print("Address infos:", ai)
    addr = ai[0][-1]

    print("DNS Response:", addr)
    s.connect(addr)

    s = ssl.wrap_socket(s)
    #print(s)

    if use_stream:
        # Both CPython and MicroPython SSLSocket objects support read() and
        # write() methods.
        s.write(get_request)  # Must be bytes instead of string
        response_bytes = s.read(4096)
    else:
        # MicroPython SSLSocket objects implement only stream interface, not
        # socket interface
        s.send(get_request)   # Must be bytes instead of string
        response_bytes = s.recv(4096)

    s.close()
    response_text = response_bytes.decode()
    #print(response_text)
    status = [ line for line in response_text.split('\r\n') if "Status" in line ]
    if status[0] == 'Status: 200 OK':
        return True
    else:
        return False


# Python equivalent to Arduino map() function of two scales:
def range_map(x, in_min, in_max, out_min, out_max):
    return (x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min


# ThingSpeak free tier limited to 15 seconds between data updates
while True:
    try:
        main()
        sleep(60)
    except:
        sleep(60)
        machine.reset()


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
f = open('key_store.db', 'r+b')
db = btree.open(f)
thingspeak_api_key = db[b'thingspeak_api_key'].decode('utf-8')
db.close()

server = 'api.thingspeak.com'


def main():
    # Read the Temperature
    tempf = read_temp()

    # Create the HTTPS GET Request string
    get_request = 'GET /update?api_key=' + thingspeak_api_key + '&field1=' + tempf + ' HTTP/1.0\r\n\r\n'
    get_request = str.encode(get_request)  # Convert Type str to bytes

    # Send the Data to ThingSpeak
    print('Sending Temp %s to %s' % (tempf, server))
    send_data(server, get_request)


def read_temp():
    adc = ADC(0)
    temp = adc.read()/10      # Divide TMP36 voltage reading by 10 for Celsius
    temp = (temp * 9/5) + 32  # Covert from Celsius to Fahrenheit
    temp = temp * 1.07        # Increase value by 7% to match TMP102 readings and actual temperature
    temp = round(temp)        # Round to remove decimals
    temp = str(temp)          # Convert to string to put into URL field1
    return temp


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

    response_text = response_bytes.decode()
    #print(response_text)
    status = [ line for line in response_text.split('\r\n') if "Status" in line ]
    print('HTTPS', status[0])

    s.close()


main()

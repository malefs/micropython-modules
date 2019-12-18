#
# Brandon Gant
# 2019-12-18
#
# Source: https://github.com/micropython/micropython/blob/master/examples/network/http_client_ssl.py
#
# Create the HTTP/HTTPS GET Request string
#   get_request = 'GET / HTTP/1.0 \r\n\r\n'
#     -OR-
#   get_request = 'GET /update?api_key=' + thingspeak_api_key + '&field1=' + str(temp) + ' HTTP/1.0\r\n\r\n'
#   get_request = str.encode(get_request)  # Convert Type str to bytes

def send_data(server, get_request, port=443, use_tls=True, use_stream=True):  # Uses HTTPS to Port 443 by Default
    import usocket as socket
    s = socket.socket()

    ai = socket.getaddrinfo(server, port)
    #print("Address infos:", ai)
    addr = ai[0][-1]

    #print("DNS Response:", addr)
    s.connect(addr)

    if use_tls:
        import ussl as ssl
        s = ssl.wrap_socket(s)
    #print(s)

    if use_stream:
        # Both CPython and MicroPython SSLSocket objects support read() and write() methods.
        s.write(get_request)  # Must be bytes instead of string
        response_bytes = s.read(4096)
    else:
        # MicroPython SSLSocket objects implement only stream interface, not socket interface.
        s.send(get_request)   # Must be bytes instead of string
        response_bytes = s.recv(4096)

    s.close()
    return response_bytes.decode()

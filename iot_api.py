from uos import uname

# api_key is usually client_id
def iot_api(server, port, api_key, field1, field2=None):
    hardware = uname().sysname

    print('Server: %s  Port: %s  API_Key: %s  Field1: %s  Field2: %s' % (server, port, api_key, field1, field2))

    # Send the field data to the iot-api server
    if 'esp32' in hardware:
        import urequests

        if '443' in port:
            transport = 'https://'
        else:
            transport = 'http://'
        URL = transport + server + ':' + port + '/update?api_key=' + api_key + '&field1=' + str(field1) + '&field2=' + str(field2)
        r = urequests.get(URL)
        response_text = r.text
        status = str(r.status_code)

    elif 'esp8266' in hardware:
        # No urequests in ESP8266 Micropython
        import http_client

        if '443' in port:
            use_tls = True
        else:
            use_tls = False

        # Create the GET Request string
        get_request = 'GET /update?api_key=' + client_id + '&field1=' + str(tempf) + ' HTTP/1.0\r\n\r\n'
        get_request = str.encode(get_request)  # Convert Type str to bytes
        response_text = http_client.send_data(server, get_request, port, use_tls)
        #print(response_text)
        status = [ line for line in response_text.split('\r\n') if "Status" in line ]
        status = status[0]

    if '200' in status:
        return True
    else:
        return False

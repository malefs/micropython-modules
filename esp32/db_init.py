# This file creates the btree.db file if it does not already exist

import btree

f = open('btree.db', 'w+b')
db = btree.open(f)

db['ssid_name'] = input('Enter WiFi SSID: ')
db['ssid_pass'] = input('Enter WiFi password: ')
db['mqtt_broker'] = input('Enter the MQTT Server IP: ')

db.flush()
print("%s, %s, and %s added to btree.db file" % (db['ssid_name'].decode('utf-8'), db['ssid_pass'].decode('utf-8'), db['mqtt_broker'].decode('utf-8')))
db.close()

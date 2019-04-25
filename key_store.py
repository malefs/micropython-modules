# MicroPython:          https://docs.micropython.org/en/latest/
#
# Brandon Gant
# 2019-03-28
#
# Usage:
#    import key_store
#    key_store.init()              <-- Creates key_store.db if it does not exist
#    key_store.set('key','value')  <-- Sets key/value in database
#    key_store.get('key')          <-- Gets value from database
#    key_store.dumptext()          <-- Prints contents of key_store.db to screen
#    key_store.dumpfile()          <-- Dumps contents of key_store.db to key_store.txt which ampy can retrieve
#    key_store.remove()            <-- Removes key_store.db file
#
# This script keeps private settings out of github and also logs everything locally if needed.
#

import btree

file = 'key_store.db'

try:
    f = open(file, 'r+b')
except OSError:
    print('WARNING: No %s on disk' % file)    

# Create a new key_store.db database or update config settings
def init():
    try:
        f = open(file, 'r+b')
    except OSError:
        f = open(file, 'w+b')
    db = btree.open(f)
    db[b'ssid_name'] = input('Enter WiFi SSID: ')
    db[b'ssid_pass'] = input('Enter WiFi password: ')
    db[b'mqtt_broker'] = input('Enter the MQTT Server IP: ')
    db.flush()
    print("%s, %s, and %s added to %s file" % (db[b'ssid_name'].decode('utf-8'), db[b'ssid_pass'].decode('utf-8'), db[b'mqtt_broker'].decode('utf-8'), file))
    db.close()

# Added new key/value pairs to key_store.db
def set(key,value):
    f = open(file, 'r+b')
    db = btree.open(f)
    db[key] = value
    db.flush()
    db.close()

# Retrieve data from key_store.db
def get(key):
    f = open(file, 'r+b')
    db = btree.open(f)
    return db[key].decode('utf-8')
    db.close()

# This just prints to the screen which is not usable in scripts.
def dumptext():
    f = open(file, 'r+b')
    db = btree.open(f)
    for key in db:
        print(key.decode('utf-8'), db[key].decode('utf-8'))
    db.close()

# Allows you to download local data: ampy -p /dev/ttyUSB0 get key_store.txt 
def dumpfile():
    f = open(file, 'r+b')
    db = btree.open(f)
    with open('key_store.txt', 'wt') as text:
        for key in db:
            pair = "{}:{}\n".format(key.decode('utf-8'), db[key].decode('utf-8'))
            text.write(pair)
    db.close()
    print('key_store.txt created')

# Removes key_store.db
def remove():
    import uos
    uos.remove(file)
    print('%s removed' % file)

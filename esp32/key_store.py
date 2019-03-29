# MicroPython:          https://docs.micropython.org/en/latest/
#
# Brandon Gant
# 2019-03-28
#
# Usage:
#    import key_store
#    key_store.update()   <-- Creates key_store.db if it does not exist
#    key_store.print()    <-- Prints contents of key_store.db to screen
#    key_store.text()     <-- Dumps contents of key_store.db to key_store.txt which ampy can retrieve
#    key_store.remove()   <-- Removes key_store.db file
#
# This script just provides a way to log everything locally if needed.
#

import btree

file = 'key_store.db'

def update():
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


# This just prints to the screen which is not usable in scripts.
def dump():
    f = open(file, 'r+b')
    db = btree.open(f)
    for key in db:
        print(key.decode('utf-8'), db[key].decode('utf-8'))
    db.close()

def text():
    f = open(file, 'r+b')
    db = btree.open(f)
    with open('key_store.txt', 'wt') as text:
        for key in db:
            pair = "{}:{}\n".format(key.decode('utf-8'), db[key].decode('utf-8'))
            text.write(pair)
    db.close()

def remove():
    import uos
    uos.remove(file)
    print('%s removed' % file)

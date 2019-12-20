# SparkFun ESP32 Thing: https://www.sparkfun.com/products/13907
# MicroPython:          http://docs.micropython.org/en/latest/library/machine.html#machine.unique_id
#
# Brandon Gant
# 2019-03-28
#
# Usage:
#    import client
#    unique_id = str(client.id())
#
# This script just returns the unique identifier from the hardware.
# 

from ubinascii import hexlify
from machine import unique_id

def id():
    client_id = hexlify(unique_id()).decode('utf-8')
    return client_id

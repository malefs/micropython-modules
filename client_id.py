# SparkFun ESP32 Thing: https://www.sparkfun.com/products/13907
# MicroPython:          http://docs.micropython.org/en/latest/library/machine.html#machine.unique_id
#
# Brandon Gant
# Created: 2019-03-28
# Updated: 2020-09-09
#
# Usage:
#    from client_id import client_id
#    print(client_id) 
#
# This script just returns the unique identifier from the hardware.
# 

from ubinascii import hexlify
from machine import unique_id
client_id = hexlify(unique_id()).decode('utf-8')  # String with Unique Client ID

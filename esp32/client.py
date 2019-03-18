import ubinascii
import machine

def id():
    client_id = ubinascii.hexlify(machine.unique_id()).decode('utf-8')
    return client_id


from machine import Pin
import client
import mqtt
import utime

# Two 10Kohm resistors in Series between 5V VUSB and GND
# Between resistors, a 2.5V wire to Pin 4
pin = Pin(4, Pin.IN)

unique_id = str(client.id())

f = open('key_store.db', 'r+b')
db = btree.open(f)

broker = db[b'mqtt_broker'].decode('utf-8')
topic = 'devices/' + unique_id

# Initialize variables and assume power is on
current_power_status = 1
last_power_status = 1

print('Monitoring Power...')
while True:
    current_power_status = pin.value()
    if current_power_status != last_power_status:
        mqtt.publish(broker, topic + '/power/timestamp', str(utime.time()))  # Epoch UTC
        mqtt.publish(broker, topic + '/power/value', str(current_power_status))
        last_power_status = current_power_status
    utime.sleep(1) 

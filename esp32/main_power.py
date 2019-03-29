
from machine import Pin
import btree
import client
import mqtt
import utime

# Two 10Kohm resistors in Series between 5V VUSB and GND
# Between resistors, a 2.5V wire to Pin 4
pin = Pin(4, Pin.IN)

# Get Unique Client ID
unique_id = str(client.id())

# Get MQTT Broker IP Address
f = open('key_store.db', 'r+b')
db = btree.open(f)
broker = db[b'mqtt_broker'].decode('utf-8')
db.close()

topic = 'devices/' + unique_id

# Initialize variables and assume power is on
current_power_status = 1
last_power_status = 1

print('Monitoring Power...')
while True:
    current_power_status = pin.value()
    if current_power_status != last_power_status:
        # Send changes to MQTT server
        timestamp = utime.time()
        mqtt.publish(broker, topic + '/power/timestamp', str(timestamp))  # Epoch UTC
        mqtt.publish(broker, topic + '/power/value', str(current_power_status))
        
        # Store values locally
        f = open('key_store.db', 'r+b')
        db = btree.open(f)
        db[str(timestamp)] = str(current_power_status) 
        db.flush()
        db.close()

        last_power_status = current_power_status

    utime.sleep(1) 


import utime
print('main.py: Press CTRL+C to drop to REPL...')
utime.sleep(3)

import tmp102
import machine
import mqtt
import client

while True:
    broker = '192.168.7.207'
    topic = 'devices/' + str(client.id())

    timestamp = str(utime.time())   # Epoch UTC
    mqtt.publish(broker, topic + '/time', timestamp) 

    temp = str(round(tmp102.read_temp('F'), 1))
    mqtt.publish(broker, topic + '/temp', temp)

    print(timestamp, temp)
    utime.sleep(1)  # Give UART time to print text before going to sleep
    machine.deepsleep(300000)


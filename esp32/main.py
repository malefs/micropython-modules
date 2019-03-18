import tmp102
import machine
import mqtt
import utime
import client

while True:
    broker = '192.168.7.207'
    topic = 'device/' + str(client.id()) + '/temp'
    message = str(round(tmp102.read_temp('F'), 1))

    mqtt.publish(broker, topic, message)

    print("Sent %s to %s... going to sleep in 3 seconds..." % (message, topic))
    utime.sleep(3)
    machine.lightsleep(10000)


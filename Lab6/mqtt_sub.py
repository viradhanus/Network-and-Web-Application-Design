import paho.mqtt.client as paho
import sys

def onMessage(client, userdata, msg):
    print(msg.topic + " : " + msg.payload.decode())

client = paho.Client()
client.on_message


if client.connect('mqtt.eclipse.org',1883,60) != 0:
    print("not connect to the broker")
    sys.exit(-1)

client.publish("test/status", "Helllo world", 0)
client.disconnect()
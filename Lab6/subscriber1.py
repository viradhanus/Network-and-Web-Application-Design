import json
import paho.mqtt.client as mqtt

tasklist = [] #list to hold the tasks


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    print(" ")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("tasks/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    msg_dict = json.loads(msg.payload.decode("utf-8"))
    # print(msg_dict)

    # if a publisher added a task
    if msg_dict['operation'] == 'ADD':
        msg_dict.pop('operation')
        print("Task added : ")
        print(msg_dict)
        tasklist.append(msg_dict)

    # if a publisher deleted a task
    elif msg_dict['operation'] == 'DELETE':
        for item in tasklist:
            if item["id"] == msg_dict["id"]:
                print("Task deleted : ")
                print(msg_dict)
                tasklist.pop(tasklist.index(item))

    # if a publisher edited a task
    elif msg_dict['operation'] == 'EDIT':
        for item in tasklist:
            if item['id'] == msg_dict['id']:
                print("Task edited : ")
                print(msg_dict)                
                item['state'] = msg_dict['state']

    # print(msg.topic + " " + str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt.eclipse.org", 1883, 60)
client.loop_forever()
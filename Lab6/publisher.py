import sys
import json
import paho.mqtt.client as mqtt
from datetime import datetime
from uuid import uuid4


def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

client.connect("mqtt.eclipse.org", 1883, 60)
client.loop_start()

if len(sys.argv) == 1:
    print("USAGE : Enter valid operation and corresponding arguments")

elif sys.argv[1] == 'ADD' and len(sys.argv) == 3:

    # create unique id based on date in Python
    task_id = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
    description = sys.argv[2]

    if len(description) < 1024:

        json_msg = {"operation": "ADD", "id": task_id, "state": "open", "description": description}
        topic = "tasks/open/add/"+task_id
        infot = client.publish(topic, json.dumps(json_msg), qos=1)
        infot.wait_for_publish()

    else:
        print("Discription is not valid")
        sys.exit (-1)

elif sys.argv[1] == 'DELETE' and len(sys.argv) == 3:
    id = sys.argv[2]
    topic = "tasks/open/DELETE/"+id
    json_msg = {"operation": "DELETE", "id": id}
    infot = client.publish(topic, json.dumps(json_msg), qos=1)
    infot.wait_for_publish()
    
# implement the EDIT operation to change task state.
elif sys.argv[1] == 'EDIT' and len(sys.argv) == 5:
    id = sys.argv[2]
    current_state = sys.argv[3]
    next_state = sys.argv[4]
    states_list = ["OPEN", "ASSIGNED", "PROGRESSING", "DONE", "CANCELLED"]
    # switch_state dictionary determines next possible states as follows
    switch_state = {    

        "OPEN": ["OPEN", "ASSIGNED", "CANCELLED"],
        "ASSIGNED" : ["ASSIGNED", "PROGRESSING"],
        "PROGRESSING":["PROGRESSING", "DONE", "CANCELLED"],
        "DONE":["DONE"],
        "CANCELLED":["CANCELLED"],
    } 
    if next_state in states_list and next_state in switch_state[current_state]:

        topic = "tasks/"+next_state+"/edit/"+id
        json_msg = {"operation": "EDIT", "id": id, "state": next_state}
        # retain flag is set to true since if a client reconnects after the edit, he should recieve the latest update 
        infot = client.publish(topic, json.dumps(json_msg), qos=1, retain=True) 
        infot.wait_for_publish()
    else:
        print("Enter valid States")
        sys.exit (-1)

else :
    print("USAGE(ADD New Task) : <ADD> <Task Description>")
    print("USAGE(DELETE a Task): <DELETE> <Task ID>")
    print("USAGE(EDIT a Task)  : <EDIT> <Task ID> <Current State> <Next State>")

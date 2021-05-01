import paho.mqtt.client as mqtt
import json

#dictionary for saving tasks
taskList = {}

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("CO324/TaskApi/sa/#")
    global taskList
    print(taskList)


#save or delete tasks in taskList based on the incomming messages
def on_message(client, userdata, msg):
    task = json.loads(msg.payload)
    #print(task)

    global taskList

    #check whether a message is about a deleted task of a new task
    
    if list(task.keys()) == ["id","state","description"]:
        if task["id"] not in taskList.keys():
            taskList[task["id"]] = task #add task to the taskList
            print("New Task added")

    elif list(task.keys()) == ["id","state"]:
        if task["id"] in taskList.keys():
            #editing a task 
            t = taskList[task["id"]]
            stats = checkState(task["state"],taskList,task["id"])
            if stats: 
                t["state"] = task["state"]
                taskList[task["id"]] = t
                client.publish("CO324/TaskApi/sa/"+str(task["id"]), payload=json.dumps(taskList[task["id"]), qos=1, retain=True)
                print("Task "+str(task["id"])+ " edited")

    elif list(task.keys()) == ["id"]:
        if task["id"] in taskList.keys():
            taskList.pop(task["id"]) #delete the task
            print("Task "+str(task["id"])+" deleted from the list")
     
    print(msg.topic+" "+str(msg.payload))
    print(taskList)

#add task function
def addTask(client,task):
  
    #publising a new task
    client.publish("CO324/TaskApi/sa/"+str(task["id"]), payload=json.dumps(task), qos=1, retain=True)
    print("New Task published")
    global taskList
    
    taskList[task["id"]] = task #add task to the local taskList


#del task function
def delTask(client,id):

    client.publish("CO324/TaskApi/sa/"+str(id), payload=json.dumps({"id":id}), qos=1, retain=True)
    print("Del Task published")

    global taskList

    if id in taskList.keys():
        taskList.pop(id) #delete the task from local storage

#editTask function
def editTask(client,id,nextState):

    task = {"id":id,"state":nextState}
    client.publish("CO324/TaskApi/sa/"+str(id), payload=json.dumps(task), qos=1, retain=True)
    print("Edit Task published")



#check for validity of a state change
def checkState(nextState,taskList,id):

    t = taskList[id]
    currentState = t["state"] #current state of the task

    if currentState == "open":
        if(nextState == "assigned") or (nextState == "cancelled"):
            return True

    elif currentState == "assigned":
        if nextState == "progersseng":
            return True
            
    elif currentState == "progressing":
        if(nextState == "cancelled") or (nextState == "done"):
            return True
    
    return False
            





client = mqtt.Client("Client1") #clean_session flag is set to False
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt.eclipse.org", 1883, 60)
task1 = {"id":1,"state":"open","description": "sample task1"}
#addTask(client,task1)
#delTask(client,1)
editTask(client,1,"cancelled")

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
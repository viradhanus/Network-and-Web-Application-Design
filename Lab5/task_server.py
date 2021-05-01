"""TODO:
    * Implement error handling in TaskapiImpl methods
    * Implement saveTasks, loadTasks
    * Implement TaskapiImpl.editTask (ignoring write conflicts)
    * Fix data race in TaskapiImpl.addTask
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import logging
from pprint import pformat
from typing import Dict, List, Mapping, Sequence, Tuple

from google.protobuf import (
    any_pb2,
    api_pb2,
    duration_pb2,
    empty_pb2,
    field_mask_pb2,
    source_context_pb2,
    struct_pb2,
    timestamp_pb2,
    type_pb2,
    wrappers_pb2,
)
from grpc import server, StatusCode
import task_pb2, task_pb2_grpc
from threading import Lock, current_thread
import grpc

# class TaskapiImpl(task_pb2_grpc.TaskapiServicer):
#     def __init__(self, taskfile: str, history_taskfile: str):
#         self.taskfile = taskfile
#         self.history_taskfile = history_taskfile
#         self.task_id = 0
#         self.mutex = Lock()



#     def __enter__(self):
#         # """Load tasks from self.taskfile"""
#         # with open(self.taskfile, mode="rb") as t:
#         #     tasklist = task_pb2.Tasks()
#         #     tasklist.ParseFromString(t.read())
#         #     logging.info(f"Loaded data from {self.taskfile}")
#         #     #create tasks dict
#         #     self.tasks: Mapping[int, task_pb2.Task] = { 
#         #         t.id: t for t in tasklist.pending 
#         #     }
#         # """Load tasks from self.history_taskfile"""
#         # with open(self.history_taskfile, mode="rb") as ht:
#         #     history_tasklist = task_pb2.Tasks()
#         #     history_tasklist.ParseFromString(ht.read())
#         #     logging.info(f"Loaded data from {self.history_taskfile}")
#         #     # create a dictionary to keep history
#         #     self.history: Mapping[int, task_pb2.Task] = { 
#         #         ht.id: [ht for ht in history_tasklist.pending] 
#         #     }

#         """Load tasks from self.taskfile"""
#         with open(self.taskfile, mode="rb") as t:
#             tasklist = task_pb2.Tasks()
#             editlog = task_pb2.Tasks()
            
#             tasklist.ParseFromString(t.read())
#             editlog.ParseFromString(lg.read())
#             logging.info(f"Loaded data from {self.taskfile}")
#             logging.info(f"Loaded data from {self.logfile}")
#             self.tasks = {}
#             self.history:Dict = {int:[List]}
#             taskid_temp : int
#             #create tasks dict
#             self.tasks: Mapping[int, task_pb2.Task] = { 
#                 t.id: t for t in tasklist.pending 
#             }
#             for log in editlog.pending:
#                 if log.id in self.history:
#                     self.history[log.id].append(log)
#                 else:
#                     self.history[log.id] = [log]
#             # self.task_id = taskid_temp +1

#         return self

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         """Save tasks to self.taskfile"""
#         with open(self.taskfile, mode="wb") as t:
#             #get all the tasks from tasks dict
#             tasks = task_pb2.Tasks(pending = self.tasks.values())
#             t.write(tasks.SerializeToString())
#             logging.info(f"Saved data to {self.taskfile}")

#             logtasks = []
#             for i in self.history.values():
#                 logtasks = logtasks + 1
#             logtasks.pop(0)
#             tasklog = task_pb2.Tasks(pending = logtasks)
#             lg.write(tasklog.SerializeToString())


        # """Save tasks to self.taskfile"""
        # with open(self.taskfile, mode="wb") as t:
        #     #get all the tasks from tasks dict
        #     tasks = task_pb2.Tasks(pending = self.tasks.values())
        #     t.write(tasks.SerializeToString())
        #     logging.info(f"Saved data to {self.taskfile}")

        # """Save tasks history to self.history_taskfile"""
        # with open(self.history_taskfile, mode="wb") as t:
        #     #get all the tasks from tasks dict
        #     tasks = task_pb2.Tasks(pending = self.tasks.values())
        #     t.write(tasks.SerializeToString())
        #     logging.info(f"Saved data to {self.history_taskfile}")

class TaskapiImpl:
    def __init__(self, taskfile: str):
        self.taskfile = taskfile
        self.task_id = 0
        self.mutex = Lock()


    def __enter__(self):
        """Load tasks from self.taskfile"""
        with open(self.taskfile, mode="rb") as t:
            tasklist = task_pb2.Tasks()
            tasklist.ParseFromString(t.read())
            logging.info(f"Loaded data from {self.taskfile}")
            self.tasks: Mapping[int, task_pb2.Task] = {}
            self.history: Mapping[int, task_pb2.Task] = {}
            # add to the dict and set id with maximum value
            for t in tasklist.pending:
                self.tasks[t.id] = t
                self.history[t.id] = []
                if self.task_id < t.id :
                    self.task_id = t.id
            self.task_id +=1
            print(f"next task id = {self.task_id}")

            with open("taskhistory.protobuf", mode="rb") as pt:
                historyTasklist = task_pb2.Tasks()
                historyTasklist.ParseFromString(pt.read())
                logging.info(f"Loaded data from taskhistory.protobuf")
                # add to the dict
                for task in historyTasklist.pending:
                    self.history[task.id].append(task)
                    print(self.history[task.id])
            
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Save tasks to self.taskfile"""
        with open(self.taskfile, mode="wb") as t:
            tasks = task_pb2.Tasks(pending=self.tasks.values())
            t.write(tasks.SerializeToString())
            logging.info(f"Saved data to {self.taskfile}")

        with open("taskhistory.protobuf", mode="wb") as pt:
            for taskList in self.history.values():
                tasks = task_pb2.Tasks(pending=taskList)
                pt.write(tasks.SerializeToString())
            logging.info(f"Saved data to taskhistory.protobuf\n")

    def addTask(self, request: wrappers_pb2.StringValue, context) -> task_pb2.Task:
        # Add error handling to descriptions
        if len(request.value) > 1024:
            context.set_details("Description is not valid")
            context.set_code(grpc.StatusCode.OUT_OF_RANGE)
            return task_pb2.Task()

        # Fix data race in TaskapiImpl.addTask
        with self.mutex as lock: 
            logging.debug(f"addTask parameters {pformat(request)}")
            t = task_pb2.Task(id=self.task_id, description=request.value, state = 'OPEN')
            self.tasks[self.task_id] = t
            self.task_id += 1
            return t

    def delTask(self, request: wrappers_pb2.UInt64Value, context) -> task_pb2.Task:
       
        # error handling, id
        if request.value in self.tasks:
            logging.debug(f"delTask parameters {pformat(request)}")
            return self.tasks.pop(request.value)
        else:
            context.set_details("ID is not valid")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return task_pb2.Task()

    def nondestructive_editTask(self, request: task_pb2.Task, context) -> task_pb2.Task:
      
        if request.id in self.tasks:

            if len(request.description) <= 1024:
                logging.debug(f"nondestruct_editTask parameters {pformat(request.description)}")
                t = task_pb2.Task(id=request.id, description=request.description)

                if request.id in self.history:
                    # append current task to the history dict 
                    self.history[request.id].append(t)

                else:
                    temp_task_list = [] #create a tempory list to hold a task
                    temp_task_list.append(t)
                    # add current task to the history dict before edit the task
                    self.history[request.id] = temp_task_list
                
                # print history dict
                print(self.history)

                # update the task
                self.tasks[request.id] = t
                return t

            else:
                # error handling, description
                context.set_details("Description is not valid")
                context.set_code(grpc.StatusCode.OUT_OF_RANGE)
                return task_pb2.Task() 
        else:
           # error handling, id
            context.set_details("ID is not valid")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return task_pb2.Task()


    def destructive_editTask(self, request: task_pb2.Task, context) -> task_pb2.Task:
       
        if request.id in self.tasks:

            if len(request.description) <= 1024:
                # deletes the task & creates a new task
                with self.mutex as lock:  # Fix data race when adding task
                    # logging.debug(f"destructive_editTask : delTask id {pformat(request.id)}")
                    self.tasks.pop(request.id)
                    logging.debug(f"destructive_editTask : addTask parameters id:{pformat(self.task_id)} => {pformat(request.description)}")
                    t = task_pb2.Task(id=self.task_id, description=request.description, state = 'OPEN',)
                    self.tasks[self.task_id] = t
                    self.task_id += 1
                    return t

            else:
                # error handling, description
                context.set_details("Description is not valid")
                context.set_code(grpc.StatusCode.OUT_OF_RANGE)
                return task_pb2.Task() 
        else:
           # error handling, id
            context.set_details("ID is not valid")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return task_pb2.Task()

    def editTask(self, request: task_pb2.Task, context) -> task_pb2.Task:
      
        if request.id in self.tasks and len(request.description) <= 1024:

            current_task_description = self.tasks[request.id].description
            current_state = self.tasks[request.id].state

            # states_list contains ["OPEN", "ASSIGNED", "PROGRESSING", "DONE", "CANCELLED"] as follows
            states_list = [0,1,2,3,4]

            # switch_state dictionary determines next possible states as follows

            # {    
            #     "OPEN": ["OPEN", "ASSIGNED", "CANCELLED"],
            #     "ASSIGNED" : ["ASSIGNED", "PROGRESSING"],
            #     "PROGRESSING":["PROGRESSING", "DONE", "CANCELLED"],
            #     "DONE":["DONE"],
            #     "CANCELLED":["CANCELLED"],
            # }   

            switch_state = {
                0:[0,1,4],
                1:[1,2],
                2:[2,3,4],
                3:[3],4:[4]
            }


            # client updates only the task description
            if bool(request.description) and not bool(request.state):

                t = task_pb2.Task(id=request.id, description=request.description, state=current_state)
                logging.debug(f"editTask parameters {pformat(request.description)}")
                self.tasks[request.id] = t
                return t

            # client updates only the task state
            if not bool(request.description) and bool(request.state):

                next_state = request.state

                # check next_state is valid state and next_state holds legal state transition
                if next_state in states_list and next_state in switch_state[current_state]: 

                    t = task_pb2.Task(id=request.id, description=current_task_description, state=next_state)
                    logging.debug(f"editTask parameters {pformat(next_state)}")
                    self.tasks[request.id] = t
                    return t
                
                else:
                    # error handling, state
                    context.set_details("State is Invalid")
                    context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                    return task_pb2.Task()                 

            # client updates both task description and task state
            if bool(request.description) and bool(request.state):

                next_state = request.state
                edited_description = request.description

                # check next_state is valid state and next_state holds legal state transition
                if next_state in states_list and next_state in switch_state[current_state]: 

                    t = task_pb2.Task(id=request.id, description=edited_description, state=next_state)
                    logging.debug(f"editTask parameters {pformat(edited_description)} {pformat(next_state)}")
                    self.tasks[request.id] = t
                    return t
                
                else:
                    # error handling, state
                    context.set_details("State is Invalid")
                    context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                    return task_pb2.Task()   
           
            # client does not update both task description and task state
            # if not bool(request.description) and not bool(request.state):

            #     t = task_pb2.Task(id=request.id, description=current_task_description, state=current_state)
            #     logging.debug(f"editTask parameters : NONE")
            #     self.tasks[request.id] = t
            #     return t

        elif request.id in self.tasks:
            # error handling, description
            context.set_details("Description is not valid")
            context.set_code(grpc.StatusCode.OUT_OF_RANGE)
            return task_pb2.Task() 

        else:
           # error handling, id
            context.set_details("ID is not valid")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return task_pb2.Task()

    def listTasks(self, request: task_pb2.TaskQuery, context) -> task_pb2.Tasks:
        logging.debug(f"listTasks parameters {pformat(request)}")
        # return a list of tasks that are in the specified states
        if len(request.selected) != 0:
            # for state in request.selected:
            #     task_list = [i for i in self.tasks.values() if i.state == state]
            # return task_pb2.Tasks(pending=task_list)
            return task_pb2.Tasks(pending=[i for i in self.tasks.values() if i.state in request.selected])

        else:
            return task_pb2.Tasks(pending=self.tasks.values())


# TASKFILE = "tasklist.protobuf"
# HISTORY_TASKFILE = "history_tasklist.protobuf"
# if __name__ == "__main__":
#     Path(TASKFILE).touch()
#     Path(HISTORY_TASKFILE).touch()
#     logging.basicConfig(level=logging.DEBUG)

#     with ThreadPoolExecutor(max_workers=1) as pool, TaskapiImpl(
#         TASKFILE, HISTORY_TASKFILE
#     ) as taskapiImpl:
#         taskserver = server(pool)
#         task_pb2_grpc.add_TaskapiServicer_to_server(taskapiImpl, taskserver)
#         taskserver.add_insecure_port("[::]:50051")
#         try:
#             taskserver.start()
#             logging.info("Taskapi ready to serve requests")
#             taskserver.wait_for_termination()
#         except:
#             logging.info("Shutting down server")
#             taskserver.stop(None)

TASKFILE = "tasklist.protobuf"
HISTORYFILE = "history.protobuf"
if __name__ == "__main__":
    Path(TASKFILE).touch()
    Path(HISTORYFILE).touch()
    logging.basicConfig(level=logging.DEBUG)

    with ThreadPoolExecutor(max_workers=1) as pool, TaskapiImpl(
        TASKFILE
    ) as taskapiImpl:
        taskserver = server(pool)
        task_pb2_grpc.add_TaskapiServicer_to_server(taskapiImpl, taskserver)
        taskserver.add_insecure_port("[::]:50051")
        try:
            taskserver.start()
            logging.info("Taskapi ready to serve requests")
            taskserver.wait_for_termination()
        except:
            logging.info("Shutting down server")
            taskserver.stop(None)

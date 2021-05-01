import logging
from concurrent.futures import ThreadPoolExecutor
from grpc import server
import task_pb2, task_pb2_grpc


class TaskapiImpl(task_pb2_grpc.TaskapiServicer):
    """Implementation of the Taskapi service"""

    def __init__(self):
        # initialise a Tasks attribute to store our tasks.
        self.Tasks = task_pb2.Tasks()
        # pass

    def addTask(self, request, context):
        logging.info(f"adding task {request.description}")
        # TODO: implement this!

        # get the length of tasks
        length = len(self.Tasks.tasks) 

        #decide the index according to the length of tasks
        if(length == 0):
            adding_task = task_pb2.Task(id=length, description=request.description)
        else:
        #append the task with the id and recieved description
            adding_id = self.Tasks.tasks[length-1].id + 1
            adding_task = task_pb2.Task(
                id=adding_id, description=request.description)

        self.Tasks.tasks.append(adding_task)
        #return id
        return task_pb2.Id(id=adding_task.id)


    def delTask(self, request, context):
        logging.info(f"deleting task {request.id}")
        # TODO: implement this!

        for i in range(len(self.Tasks.tasks)):
            if(self.Tasks.tasks[i].id == request.id):
                deleting_task = self.Tasks.tasks[i] #record deleting task
                self.Tasks.tasks.pop(i) #delete the requested task
                return task_pb2.Task(id=deleting_task.id, description=deleting_task.description)

        print("Task does not exist")
        return

    def listTasks(self, request, context):
        logging.info("returning task list")
        # TODO: implement this!
        
        return self.Tasks


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    taskserver = server(ThreadPoolExecutor(max_workers=10))
    task_pb2_grpc.add_TaskapiServicer_to_server(TaskapiImpl(), taskserver)
    taskserver.add_insecure_port("[::]:50051")
    try:
        taskserver.start()
        logging.info("Taskapi ready to serve requests")
        taskserver.wait_for_termination()
    except:
        logging.info("Shutting down server")
        taskserver.stop(None)
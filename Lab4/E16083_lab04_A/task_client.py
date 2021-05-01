import random
import string
import logging, grpc
import task_pb2, task_pb2_grpc

def random_string_generator(str_size, allowed_chars):
    return "".join(random.choice(allowed_chars) for x in range(str_size))


# Test that will be used to grade addTask
def test_add(stub, count):
    chars = string.ascii_letters + string.punctuation
    task_ids = []
    for i in range(count):
        desc = random_string_generator(99, chars)
        response = stub.addTask(task_pb2.TaskDesc(description=desc))
        task_ids.append(response.id)

    return task_ids


# Test that will be used to grade delTask
def test_del(stub, task_ids):
    for i in task_ids:
        response = stub.delTask(task_pb2.Id(id=i))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = task_pb2_grpc.TaskapiStub(channel)

        task_ids = test_add(stub, 10)
        print(f"Task ids {task_ids}")
        # Test that will be used to grade listTasks
        response = stub.listTasks(task_pb2.Empty())
        print(f"Task list \n{response.tasks}")
        test_del(stub, task_ids)

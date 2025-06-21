from multiprocessing import Process, current_process

def task1():
    print("Task1 started")
    print(current_process().name)
    print(current_process().pid)
    process2 = Process(target = task2, name = "process2")
    process2.start()
    process2.join()
    print("task1 finished")

def task2():
    print("Task2 started")
    print(current_process().name)
    print(current_process().pid)
    print("Task2 finished")


if __name__ == "__main__":
    process1 = Process(target = task1, name = "process1")
    process1.start()
    process1.join()
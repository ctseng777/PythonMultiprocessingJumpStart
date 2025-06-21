# SuperFastPython.com
# example of shared ctype accessed in multiple processes
from random import random
from multiprocessing import Value, Lock
from multiprocessing import Process
from time import sleep


# custom function to be executed in a child process
def task(shared_var, ident):
    sleep(1)
    # generate a single floating point value
    #generated = random()
    print(f"Process {ident} reading value: {shared_var.value}", flush=True)
    # store value
    shared_var.value += 0.1
    # report progress
    print(f'Process {ident} wrote: {shared_var.value}', flush=True)

def thread_safe_task(shared_var, ident):
    sleep(1)
    # generate a single floating point value
    #generated = random()
    
    with shared_var.get_lock():
        print(f"Process {ident} reading value: {shared_var.value}", flush=True)
        # store value
        shared_var.value += 0.1
        # report progress
        print(f'Process {ident} wrote: {shared_var.value}', flush=True)
    
    

# protect the entry point
if __name__ == '__main__':
    """
    python src/lesson05_ctypes.py
Experiment 1: Not thread safe --------------------------------
Process 2 reading value: 0.0
Process 2 wrote: 0.10000000149011612
Process 0 reading value: 0.10000000149011612
Process 4 reading value: 0.10000000149011612
Process 0 wrote: 0.20000000298023224
Process 4 wrote: 0.30000001192092896
Process 1 reading value: 0.30000001192092896
Process 1 wrote: 0.4000000059604645
Process 3 reading value: 0.4000000059604645
Process 3 wrote: 0.5
Process 7 reading value: 0.5
Process 5 reading value: 0.5
Process 7 wrote: 0.6000000238418579
Process 5 wrote: 0.6000000238418579
Process 6 reading value: 0.6000000238418579
Process 8 reading value: 0.6000000238418579
Process 6 wrote: 0.7000000476837158
Process 8 wrote: 0.7000000476837158
Process 9 reading value: 0.7000000476837158
Process 9 wrote: 0.8000000715255737
Read: 0.8000000715255737
    """
    # print("Experiment 1: Not thread safe --------------------------------")
    # # create shared variable
    # variable = Value('f', 0.0)
    # # create a child process process
    # processes = [Process(target=task, args=(variable, i)) for i in range(10)]
    # # start the process
    # for process in processes:
    #     process.start()
    # # wait for the process to finish
    # for process in processes:
    #     process.join()
    # # read the value
    # data = variable.value
    # # report the value
    # print(f'Read: {data}')


    print("Experiment 2: Thread safe --------------------------------")
    # create shared variable
    variable = Value('f', 0.0)
    
    # create a child process 
    processes = [Process(target=thread_safe_task, args=(variable, i)) for i in range(10)]
    # start the process
    for process in processes:
        process.start()
    # wait for the process to finish
    for process in processes:
        process.join()

    print(f"Read: {variable.value}")
# SuperFastPython.com
# example of wait/notify with a condition for processes
from time import sleep
from multiprocessing import Process
from multiprocessing import Condition
from multiprocessing import Value, Lock
from multiprocessing import Barrier

# custom function to be executed in a child process
def task(shared_condition):
    # block for a moment
    sleep(1)
    # notify a waiting process that the work is done
    print('Child sending notification...', flush=True)
    with shared_condition:
        shared_condition.notify()

def task2(condition, ident):
    sleep(1)
    # Notify a waiting process that the work is done
    print(f"Child {ident} sending notification...", flush=True)
    with condition:
        condition.notify()

def task3(condition, counter, lock, ident):

    print(f"Child {ident} sending notification...", flush=True)
    with lock:
        counter.value += 1
        print(f"Counter is now {counter.value}", flush=True)
    
    with condition:
        condition.notify()

def task4(barrier, ident):
    sleep(1)
    barrier.wait()
    print(f"Child {ident} passed barrier", flush=True)

# protect the entry point
if __name__ == '__main__':
    # print("Experiment 1 : ait on single notification --------------------------------")
    # # create a condition
    # condition = Condition()
    # # acquire the condition
    # print('Main process waiting for data...')
    # with condition:
    #     # create a new process to execute the task
    #     worker = Process(target=task, args=(condition,))
    #     # start the new child process
    #     worker.start()
    #     # wait to be notified by the child process
    #     condition.wait()
    # # we know the data is ready
    # print('Main process all done')

    # 2-a may run into race condition. The timing between worker.start() and condition.wait() is subtle
    # 2-a: wait on multiple notifications with proper for look--------------------------------
    print("Experiment 2-a - wait on multiple notifications with proper for loop--------------------------------")
    condition2 = Condition()
    print('Main process waiting for data...')
    with condition2: 
        workers = [Process(target=task2, args=(condition2, i)) for i in range(5)]
        for worker in workers:
            worker.start()
            condition2.wait()
            
    print("Main process all done")

    # 2-b hangs. Swapping condition.wait() and worker.start() does not help.
    #Conditions are not persistent - if you send a notification when no process is waiting, the notification is lost forever. The timing of when you call wait() vs when you call notify() is crucial in multiprocessing synchronization.

    # print("Experiment 2 - b: wait on multiple notifications with for loop --------------------------------")
    # condition3 = Condition()
    # print('Main process waiting for data...')
    # with condition3: 
    #     workers = [Process(target=task2, args=(condition3, i)) for i in range(5)]
    #     for _ in range(5):
    #         condition3.wait()
    #     for worker in workers:
    #         worker.start()
    # print("Main process all done")

    print("Experiment 2 - c: wait on multiple notifications with Counter --------------------------------")
    counter = Value('i', 0)
    condition4 = Condition()
    lock = Lock()
    print('Main process waiting for data...')

    workers = [Process(target=task3, args=(condition4, counter, lock, i)) for i in range(5)]
    for worker in workers:
        worker.start()

    with condition4: 
        while counter.value < 5:
            pass
            #print(f"Waiting... counter = {counter.value}", flush= True)
    
    print(f"All workers completed. Final counter: {counter.value}")

    for worker in workers:
        worker.join()

    print("Main process all done")


    print("Experiment 2 - c: wait on multiple notifications with Barrier --------------------------------")
    barrier = Barrier(1 + 5)
    print('Main process waiting for data...')

    workers = [Process(target=task4, args=(barrier, i)) for i in range(5)]
    for worker in workers:
        worker.start()
    barrier.wait()

    print("Main process all done")

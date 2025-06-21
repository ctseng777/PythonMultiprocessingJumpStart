# SuperFastPython.com
# example of using a barrier with processes
from time import sleep
from random import random
from multiprocessing import Process
from multiprocessing import Barrier
import time


"""
A Barrier is a synchronization primitive that ensures multiple processes (or threads) reach a specific point before any of them can proceed further. Think of it as a "meeting point" where all processes must arrive before anyone can continue.
What Barriers Are For:
1. Synchronization
Barriers coordinate multiple processes to ensure they all complete a certain phase before moving to the next phase.
2. Phase-Based Processing
They're perfect for algorithms that have distinct phases where all processes must finish one phase before starting the next.
3. Parallel Processing Coordination
When you need all worker processes to complete their work before the main process continues.
"""

"""
What flush=True Does:
The flush=True parameter forces Python to immediately write the output to the console instead of buffering it. Without it, the output might be delayed or appear out of order.
Why It's Necessary in Multiprocessing:
1. Output Buffering Issues
In multiprocessing, each process has its own output buffer. Without flush=True:
Output might be held in memory buffers
Messages could appear delayed or in unexpected order
Some output might not appear at all until the process ends
2. Real-Time Visibility
With flush=True:
Apply to lesson04_bar...
)
Each process's output appears immediately when it's generated
You can see the progress of each worker process in real-time
The output order reflects the actual completion order of processes
3. Debugging and Monitoring
In your barrier example, you want to see:
Which process finishes first
The actual timing of when each process completes
Real-time progress as processes reach the barrier
"""


# custom function to be executed in a child process
def task(shared_barrier, ident):
    start = time.perf_counter()
    # generate a unique value between 0 and 10
    value = random() * 10
    # block for a moment
    sleep(value)
    # report result
    print(f'Process {ident} got: {value}', flush=True)
    # wait for all other processes to complete
    shared_barrier.wait()
    end = time.perf_counter()
    print(f"Process {ident} returns after {end - start} seconds")


def task_no_barrier(ident):
    start = time.perf_counter()
    value = random() * 10
    sleep(value)
    print(f'Process {ident} got: {value}', flush=True)
    end = time.perf_counter()
    print(f"Process {ident} returns after {end - start} seconds")

# protect the entry point
if __name__ == '__main__':
    # create a barrier for (5 workers + 1 main process)
    barrier = Barrier(5 + 1)
    # create the worker processes
    workers = [Process(target=task,
        args=(barrier, i)) for i in range(5)]
    # start the worker processes
    for worker in workers:
        # start process
        worker.start()
    # wait for all worker processes to finish
    print('Main process waiting on all results...')
    barrier.wait()
    # report once all processes are done
    print('All processes have their result')


    print("No barrier experiment")
    workers = [Process(target=task_no_barrier, 
        args = (i,)) for i in range(5)]
    for worker in workers:
        worker.start()
    print("No barrier workers started")
    for worker in workers:
        worker.join()
    print('All processes have their result')

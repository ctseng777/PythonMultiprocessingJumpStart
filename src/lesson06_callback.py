# SuperFastPython.com
# example of a callback function for a one-off task
from random import random
from time import sleep
from multiprocessing import Pool
from multiprocessing import current_process

# result callback function
# Callback is executed by parent process which creates the pool
"""
Callback Location: The callback runs in the same process that created the Pool and called apply_async()
Process Isolation: Each process has its own memory space, so callbacks are isolated to their creating process
No Cross-Process Callbacks: A callback cannot be executed by a different process than the one that submitted the task
Pool Scope: Each Pool is tied to the process that created it
"""
def result_callback(return_value):
    print(f"In callback,current process: {current_process()}")
    # report a message
    print(f'Callback got: {return_value}', flush=True)

# custom function to be executed in a child process
def task(ident):
    print(f"Current process: {current_process()}")
    # generate a value
    value = random()
    # report a message
    print(f'Task {ident} with {value}', flush=True)
    # block for a moment
    sleep(value)
    # return the generated value
    return value

# protect the entry point
if __name__ == '__main__':
    # create and configure the multiprocessing pool
    with Pool() as pool:
        # issue tasks to the multiprocessing pool
        result = pool.apply_async(task, args=(0,),
            callback=result_callback)
        # close the multiprocessing pool
        pool.close()
        print("Pool closed")
        # wait for all tasks to complete
        pool.join()
        print("Pool joined")

"""
The Sequence of Events:
Pool is created and task is submitted with apply_async()
Pool.close() is called - this prevents new tasks from being submitted
"Pool closed" is printed
Task executes in a worker process (this happens asynchronously)
Task prints its value
Callback executes in the main process when task completes
"Pool joined" is printed after all tasks finish
"""

"""
No, you cannot use callbacks directly with Process objects. Here's why:
Key Differences:
Pool.apply_async() with callbacks:
Apply to lesson06_cal...
)
Process objects:
Apply to lesson06_cal...
option
Why Pool supports callbacks but Process doesn't:
Pool is designed for task-based parallelism with built-in result handling
It manages a pool of worker processes
It automatically handles result collection and callback execution
The callback runs in the main process when the task completes
Process is a lower-level primitive for creating individual processes
It doesn't have built-in result handling
It doesn't automatically collect return values
It doesn't have callback mechanisms
"""
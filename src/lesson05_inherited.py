# SuperFastPython.com
# example of sharing global between forked processes
from multiprocessing import Process
from multiprocessing import set_start_method

"""
When you use the 'fork' start method on Unix-like systems (like macOS), the child process gets a copy of the parent process's memory space at the moment of forking. This means:
Initial state: Both parent and child start with data = 'Hello there'
Child process modification: The child process changes its copy of data to 'hello hello!'
Parent process remains unchanged: The parent process still has its original copy with data = 'Hello there'
Here's what happens step by step:
Before fork: data = 'Hello there' exists in the main process
Fork occurs: The child process gets an exact copy of the parent's memory, including the global variable data
Child process runs: It sees data = 'Hello there', then changes its copy to 'hello hello!'
Parent process continues: It still has its original copy of data = 'Hello there'
This is the fundamental behavior of process isolation in multiprocessing. Each process has its own memory space, and changes in one process don't affect the memory of other processes, even when using fork which creates an initial copy.
If you wanted to share data between processes, you would need to use other multiprocessing mechanisms like:
multiprocessing.Value or multiprocessing.Array for shared memory
multiprocessing.Queue for message passing
multiprocessing.Manager for managed objects
The fork method just determines how the child process is created, but once created, each process has its own isolated memory space.
"""

# custom function to be executed in a child process
def task():
    # declare global state
    global data
    # report global state
    print(f'child process before: {data}', flush=True)
    # change global state
    data = 'hello hello!'
    # report global state
    print(f'child process after: {data}', flush=True)

# protect the entry point
if __name__ == '__main__':
    # set the start method to fork
    set_start_method('fork')
    # define global state
    data = 'Hello there'
    # report global state
    print(f'main process: {data}')
    # start a child process
    process = Process(target=task)
    process.start()
    # wait for the child to terminate
    process.join()
    # report global state
    print(f'main process: {data}')

# SuperFastPython.com
# example of setting a process to be a daemon
from multiprocessing import Process

"""
A daemon process is a background process that runs independently of the main program and typically provides a service or performs tasks without requiring user interaction. In the context of Python's multiprocessing module, daemon processes have some important characteristics:
Key Properties of Daemon Processes:
Background Execution: Daemon processes run in the background and don't block the main program from exiting.
Automatic Termination: When the main process (parent) exits, all daemon child processes are automatically terminated, regardless of whether they have completed their work.
Non-Blocking: The main program doesn't wait for daemon processes to finish before exiting.

"""


# protect the entry point
if __name__ == '__main__':
    # create a daemon process
    process = Process(daemon=True)
    # report if the process is a daemon
    print(process.daemon)

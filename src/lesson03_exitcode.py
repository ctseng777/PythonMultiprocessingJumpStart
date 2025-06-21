# SuperFastPython.com
# example of checking the exit status of a child process
from time import sleep
from multiprocessing import Process

# custom function to be executed in a child process
def task():
    # block for a moment
    sleep(1)

def task2():
    raise Exception('This is an error')

# protect the entry point
if __name__ == '__main__':
    # create the process
    print("Process 1")
    process = Process(target=task)
    # report the exit status
    print(process.exitcode)  # None
    # start the process
    process.start()
    # report the exit status
    print(process.exitcode)  # None
    # wait for the process to finish
    process.join()
    # report the exit status
    print(process.exitcode) # 0


    print("Process 2")
    process2 = Process(target=task2)
    print(process2.exitcode) # None
    process2.start()
    print(process2.exitcode) # None
    process2.join()
    print(process2.exitcode) #1

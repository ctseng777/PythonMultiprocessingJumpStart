# SuperFastPython.com
# example of executing an async one-off task
from multiprocessing import Pool, Process
from time import sleep

# custom function to be executed in a child process
def task(ident):
    # report a message
    for i in range(10):
        print(f'Process {ident} prints {i}', flush=True)
        sleep(1)

# protect the entry point
if __name__ == '__main__':
    # create the multiprocessing pool
    # print("Experiment 1 async using pool --------------------------------")
    # with Pool() as pool:
    #     # issue a task asynchronously
    #     async_result = pool.apply_async(task, args=(0,))

    #     # Do other work while task runs
    #     for i in range(15):
    #         print(f"Main process prints {i}", flush=True)
    #         sleep(1)

    #     # wait for the task to complete
    #     async_result.wait()

    # print("Experiment 2 async using process --------------------------------")
    # process = Process(target=task, args=(0,))
    # process.start()
    # # Do other work while task runs
    # for i in range(15):
    #     print(f"Main process prints {i}", flush=True)
    #     sleep(1)

    # process.join()

    # print("Experiment 3 sync using pool --------------------------------")
    # with Pool() as pool:
    #     pool.apply(task, args=(0,))
    #     for i in range(15):
    #         print(f"Main process prints {i}", flush=True)
    #         sleep(1)

    print("Experiment 4 sync using process --------------------------------")
    process = Process(target=task, args=(0,))
    process.start()
    process.join()
    for i in range(15):
        print(f"Main process prints {i}", flush=True)
        sleep(1)

    
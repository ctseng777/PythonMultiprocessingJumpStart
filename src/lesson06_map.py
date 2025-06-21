# SuperFastPython.com
# example executing multiple tasks with different args
from multiprocessing import Pool

# custom function to be executed in a child process
def task(arg):
    # report a message
    print(f'Worker task got {arg}', flush=True)
    # return a value
    return arg * 2

def task2_wrapper(args):
    arg1, arg2 = args
    return task2(arg1, arg2)

def task2(arg1, arg2):
    print(f"Worker task2 received {arg1} and {arg2}")
    return arg1 + arg2

# protect the entry point
if __name__ == '__main__':
    # create the multiprocessing pool
    with Pool() as pool:
        # issue multiple tasks and process return values
        for result in pool.map(task, range(10)):
            # report result
            print(result)

    # Use wrapper function
    with Pool() as pool:
        for result in pool.map(task2_wrapper, zip(range(10), range(10))):
            print(result)

    with Pool() as pool:
        # Use starmap for functions with multiple arguments
        # Prepare arguments as tuples
        args = [(i, i*2) for i in range(10)]
        for result in pool.starmap(task2, args):
            print(result)
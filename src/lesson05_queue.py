# SuperFastPython.com
# example of producer and consumer processes with queue
from time import sleep
from random import random
from multiprocessing import Process
from multiprocessing import Queue

# custom function for generating work (producer)
def producer(shared_queue):
    print('Producer: Running', flush=True)
    # generate work
    for _ in range(10):
        # generate a value
        value = random()
        # block
        sleep(value)
        # add to the queue
        shared_queue.put(value)
    # all done
    shared_queue.put(None)
    shared_queue.put(None)
    print('Producer: Done', flush=True)

# custom function for consuming work (consumer)
def consumer(shared_queue, ident):
    print(f'Consumer {ident}: Running', flush=True)
    # consume work
    while True:
        # get a unit of work
        item = shared_queue.get()
        # check for stop
        if item is None:
            break
        # report
        print(f'>Consumer {ident} got {item}', flush=True)
    # all done
    print(f'Consumer {ident}: Done', flush=True)

# protect the entry point
if __name__ == '__main__':
    # create the shared queue
    queue = Queue()
    # start the consumer
    consumer_p = Process(target=consumer, args=(queue, 0))
    consumer_p.start()
    consumer_p2 = Process(target=consumer, args=(queue, 1))
    consumer_p2.start()
    # start the producer
    producer_p = Process(target=producer, args=(queue,))
    producer_p.start()
    # wait for all processes to finish
    producer_p.join()
    consumer_p.join()


"""
Thread Safety
multiprocessing.Queue is designed to be:
Thread-safe: Multiple threads can safely put/get items from the same queue
Process-safe: Multiple processes can safely put/get items from the same queue
FIFO (First-In-First-Out): Items are retrieved in the order they were added
How It Works
The multiprocessing.Queue uses:
Internal locking mechanisms to prevent race conditions
Process-safe communication through pipes or shared memory
Automatic serialization of Python objects when passing between processes
Key Features
Atomic operations: put() and get() operations are atomic
Blocking by default: get() blocks until an item is available
Timeout support: You can specify timeouts for non-blocking operations
Size limits: You can set a maximum size to prevent memory issues
"""
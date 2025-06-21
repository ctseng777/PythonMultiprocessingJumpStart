# SuperFastPython.com
# example of using an event object with processes
from time import sleep
from random import random
from multiprocessing import Process
from multiprocessing import Event
import time
from logging import getLogger, basicConfig, INFO

basicConfig(level=INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = getLogger(__name__)

# custom function to be executed in a child process
def task(shared_event, number):
    # wait for the event to be set
    print(f'Process {number} waiting...', flush=True)
    shared_event.wait()
    print(f"Process resuming at {time.perf_counter()}")
    # begin processing, generate a random number
    value = random()
    # block for a fraction of a second
    sleep(value)
    # report a message
    print(f'Process {number} got {value}', flush=True)

# Order dependent events
def task_with_2_events(event, event2):
    print(f"Starting to wait for events...", flush=True)
    print(f"event is_set = {event.is_set()}, event2 is_set = {event2.is_set()}", flush=True)
    
    # Wait for first event
    print("Waiting for event 1...", flush=True)
    event.wait()
    print(f"Event 1 triggered at {time.perf_counter()}", flush=True)
    
    # Wait for second event
    print("Waiting for event 2...", flush=True)
    event2.wait()
    print(f"Event 2 triggered at {time.perf_counter()}", flush=True)
    
    print("Both events triggered, task complete!", flush=True)

def task_with_2_events_order_independent(event, event2):
    logger.info(f"Starting to wait for events...")
    logger.info(f"event is_set = {event.is_set()}, event2 is_set = {event2.is_set()}")
    
    logger.info("Waiting for event 1...")
    event.wait()
    logger.info("Waiting for event 2...")
    event2.wait()

    # Wait for both events to be set
    while True:
        if event.is_set() and event2.is_set():
            break
    
    logger.info("Both events triggered, task complete!")

# protect the entry point
if __name__ == '__main__':
    # # create a shared event object
    # event = Event()
    # # create a suite of processes
    # processes = [Process(target=task,
    #     args=(event, i)) for i in range(5)]
    # # start all processes
    # for process in processes:
    #     process.start()
    # # block for a moment
    # print(f"Main process blocking at {time.perf_counter()}")
    # sleep(2)
    # # trigger all child processes
    # event.set()
    # # wait for all child processes to terminate
    # for process in processes:
    #     process.join()


    # # wait on 2 events - order dependent
    # print("Experiment 2 --------------------------------")
    # event.clear()
    # event2 = Event()
    # print(f"event.is_set() = {event.is_set()}")
    # print(f"event2.is_set() = {event2.is_set()}")

    # process = Process(target=task_with_2_events, args=(event, event2))
    # process.start()

    # sleep(3)
    # event.set()

    # #process.join()

    # sleep(3)
    # event2.set()

    # process.join()

    # wait on 2 events - order independent
    print("Experiment 3 --------------------------------")
    event = Event()
    event2 = Event()
    print(f"event.is_set() = {event.is_set()}")
    print(f"event2.is_set() = {event2.is_set()}")

    process = Process(target=task_with_2_events_order_independent, args=(event, event2))
    process.start()

    sleep(3)
    event2.set()

    #process.join()

    sleep(3)
    event.set()

    process.join()
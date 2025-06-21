# SuperFastPython.com
# example of using a pipe between processes
from time import sleep
from random import random
from multiprocessing import Process
from multiprocessing import Pipe

# custom function generate work items (sender)
def sender(connection):
    print('Sender: Running', flush=True)
    # generate work
    for _ in range(10):
        # generate a value
        value = random()
        # block
        sleep(value)
        # send data
        connection.send(value)
    # all done, signal to expect no further messages
    connection.send(None)
    print('Sender: Done', flush=True)

# custom function to consume work items (receiver)
def receiver(connection, ident):
    print(f"Receiver {ident}: Running", flush=True)
    # consume work
    while True:
        # get a unit of work
        item = connection.recv()
        # report
        print(f'>receiver {ident} got {item}', flush=True)
        # check for stop
        if item is None:
            break
    # all done
    print(f"Receiver {ident}: Done", flush=True)

# protect the entry point
if __name__ == '__main__':
    # create the pipe
    conn1, conn2 = Pipe()
    # start the sender
    sender_p = Process(target=sender, args=(conn2,))
    sender_p.start()
    # start the receiver
    receiver_p = Process(target=receiver, args=(conn1, 0))
    receiver_p2 = Process(target=receiver, args=(conn1, 1))
    receiver_p.start()
    receiver_p2.start()
    # wait for all processes to finish
    sender_p.join()
    receiver_p.join()
    receiver_p2.join()

"""
The Problem
When you have multiple processes reading from the same pipe connection (conn1), you'll encounter race conditions. Here's what happens:
Only one message per send: The sender sends one message at a time
First-come-first-served: Whichever receiver calls connection.recv() first will get the message
Unpredictable distribution: You can't control which receiver gets which message
Potential deadlock: If one receiver gets the None signal first, the other receiver might hang forever
"""
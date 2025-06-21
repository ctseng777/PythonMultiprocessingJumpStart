# SuperFastPython.com
# example of assessing whether a process is alive
from multiprocessing import Process

# protect the entry point
if __name__ == '__main__':
    # create the process
    process = Process()
    # report the process is alive
    print(process.is_alive()) #False

    process.start()
    print(process.is_alive()) # True

    process.join()
    print(process.is_alive()) # False

    process2 = Process()
    process2.start()
    print(process2.is_alive()) # True
    """
    The reason process2.is_alive() returns True immediately after process2.kill() is due to the asynchronous nature of process termination in multiprocessing. 
    Why This Happens:
    Signal Handling: The kill() method sends a SIGTERM signal to the process
    Graceful Termination: The process receives the signal and begins its shutdown sequence
    Time Lag: There's a brief period between when the signal is sent and when the process actually terminates
    State Check: is_alive() checks the current state, which may still be "alive" during this transition period

    you need to call join() after kill() to wait for the process to actually terminate
    """
    process2.kill()
    print(process2.is_alive()) # True
    print(process2.exitcode) # None
    process2.join()
    print(process2.is_alive()) # False
    print(process2.exitcode) # 9 Exit Code 9: SIGKILL Signal

"""
Signal-Based Termination (Negative numbers):
-1: SIGHUP (Hangup)
-2: SIGINT (Interrupt - Ctrl+C)
-3: SIGQUIT (Quit)
-9: SIGKILL (Kill - cannot be caught or ignored)
-15: SIGTERM (Termination - graceful shutdown)
"""
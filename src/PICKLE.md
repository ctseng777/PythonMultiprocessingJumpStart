# Pickling Limitations in Python Multiprocessing

## What is Pickling?

Pickling is Python's built-in serialization mechanism that converts Python objects into a byte stream. When using multiprocessing, all data passed between processes must be serialized (pickled) because processes have separate memory spaces.

## The Core Problem

**ProcessPoolExecutor** (and all multiprocessing) requires that:

1. Functions to be executed must be picklable
2. Arguments passed to functions must be picklable
3. Return values must be picklable

## What CAN Be Pickled

✅ **Built-in Python types:**

- Numbers (int, float, complex)
- Strings (str, bytes)
- Collections (list, tuple, dict, set)
- Booleans (True, False)
- None

✅ **Module-level functions:**

```python
def my_function(x):  # ✅ Can be pickled
    return x * 2
```

✅ **Classes defined at module level:**

```python
class MyClass:  # ✅ Can be pickled
    def __init__(self, value):
        self.value = value
```

✅ **Instances of picklable classes:**

```python
obj = MyClass(10)  # ✅ Can be pickled
```

✅ **functools.partial objects:**

```python
from functools import partial
partial_func = partial(my_function, 5)  # ✅ Can be pickled
```

## What CANNOT Be Pickled

❌ **Local functions (defined inside other functions):**

```python
def outer_function():
    def local_function(x):  # ❌ Cannot be pickled
        return x * 2
    return local_function
```

❌ **Lambda functions:**

```python
lambda x: x * 2  # ❌ Cannot be pickled
```

❌ **Functions with closures:**

```python
def create_closure():
    local_var = 10
    def closure_func(x):
        return x + local_var  # ❌ Captures local_var
    return closure_func
```

❌ **Objects with file handles:**

```python
class BadClass:
    def __init__(self):
        self.file = open('file.txt', 'r')  # ❌ File handle not picklable
```

❌ **Network connections, database connections:**

```python
import socket
sock = socket.socket()  # ❌ Network objects not picklable
```

❌ **Threading objects:**

```python
import threading
lock = threading.Lock()  # ❌ Threading objects not picklable
```

## The Error You Encountered

Your error occurred because:

```python
def callback_example():
    def task_with_callback(task_id):  # ❌ LOCAL FUNCTION
        # ... function body
```

The function `task_with_callback` was defined **inside** the `callback_example` function, making it a local function that cannot be pickled.

## Why This Happens

1. **ProcessPoolExecutor** needs to send the function to worker processes
2. **Worker processes** run in separate memory spaces
3. **Functions must be serialized** to travel between processes
4. **Local functions** depend on their enclosing scope, which doesn't exist in worker processes
5. **Pickling fails** because the function's context cannot be reconstructed

## Solutions

### 1. Move Functions to Module Level

```python
# ✅ Define at module level
def task_with_callback(task_id):
    return task_id * 2

def callback_example():
    with ProcessPoolExecutor() as executor:
        future = executor.submit(task_with_callback, 5)
```

### 2. Use functools.partial

```python
from functools import partial

def module_function(x, multiplier):
    return x * multiplier

def callback_example():
    with ProcessPoolExecutor() as executor:
        # Create picklable partial function
        task = partial(module_function, multiplier=10)
        future = executor.submit(task, 5)
```

### 3. Pass Data as Arguments

```python
def module_function(x, multiplier):
    return x * multiplier

def callback_example():
    with ProcessPoolExecutor() as executor:
        # Pass multiplier as argument
        future = executor.submit(module_function, 5, 10)
```

## Testing Picklability

You can test if an object is picklable:

```python
import pickle

def test_picklability(obj):
    try:
        pickle.dumps(obj)
        print("✅ Object is picklable")
        return True
    except Exception as e:
        print(f"❌ Object is NOT picklable: {e}")
        return False
```

## Best Practices

1. **Always define functions at module level** when using multiprocessing
2. **Use `functools.partial`** for additional arguments
3. **Pass data as arguments** rather than capturing in closures
4. **Avoid lambda functions** in multiprocessing
5. **Test picklability** before using in multiprocessing
6. **Use simple data structures** (lists, dicts, tuples)
7. **Avoid objects with external resources** (files, network connections)

## Key Takeaway

The fundamental rule: **Everything passed between processes must be picklable**. This includes functions, arguments, and return values. When in doubt, define functions at the module level and pass data as explicit arguments.

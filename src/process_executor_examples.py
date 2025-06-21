# SuperFastPython.com
# Comprehensive ProcessExecutor examples
from concurrent.futures import ProcessPoolExecutor, as_completed
from time import sleep, time
from random import random, randint
import os
import sys

# Example 1: Basic ProcessExecutor usage
def basic_task(task_id):
    """Basic task that simulates work"""
    sleep(random() * 2)  # Random sleep between 0-2 seconds
    result = task_id * 2
    print(f"Task {task_id} completed by process {os.getpid()}")
    return result

def basic_process_executor():
    """Demonstrate basic ProcessExecutor usage"""
    print("=== Basic ProcessExecutor Example ===")
    
    # Create a ProcessPoolExecutor with 4 worker processes
    with ProcessPoolExecutor(max_workers=4) as executor:
        # Submit tasks and get futures
        futures = []
        for i in range(8):
            future = executor.submit(basic_task, i)
            futures.append(future)
        
        # Collect results
        results = []
        for future in futures:
            result = future.result()  # This blocks until task completes
            results.append(result)
            print(f"Got result: {result}")
    
    print(f"All results: {results}")
    print()

# Example 2: Using map() for parallel processing
def map_task(x):
    """Task for map operation"""
    sleep(0.1)  # Simulate work
    return x * x

def process_executor_map():
    """Demonstrate ProcessExecutor map() method"""
    print("=== ProcessExecutor Map Example ===")
    
    data = list(range(20))
    
    with ProcessPoolExecutor(max_workers=4) as executor:
        # Map function over data in parallel
        results = list(executor.map(map_task, data))
    
    print(f"Input: {data[:10]}...")  # Show first 10
    print(f"Output: {results[:10]}...")  # Show first 10
    print()

# Example 3: Using as_completed() for non-blocking results
def async_task(task_id):
    """Task that takes variable time"""
    duration = random() * 3
    sleep(duration)
    return f"Task {task_id} completed in {duration:.2f}s"

def process_executor_as_completed():
    """Demonstrate as_completed() for non-blocking results"""
    print("=== ProcessExecutor as_completed Example ===")
    
    with ProcessPoolExecutor(max_workers=3) as executor:
        # Submit all tasks
        futures = {executor.submit(async_task, i): i for i in range(6)}
        
        # Process results as they complete
        for future in as_completed(futures):
            task_id = futures[future]
            try:
                result = future.result()
                print(f"Completed: {result}")
            except Exception as e:
                print(f"Task {task_id} generated an exception: {e}")
    
    print()

# Example 4: Error handling and exceptions
def error_task(task_id):
    """Task that may raise an exception"""
    if task_id % 3 == 0:  # Every 3rd task fails
        raise ValueError(f"Task {task_id} failed intentionally")
    
    sleep(random())
    return f"Task {task_id} succeeded"

def process_executor_error_handling():
    """Demonstrate error handling in ProcessExecutor"""
    print("=== ProcessExecutor Error Handling Example ===")
    
    with ProcessPoolExecutor(max_workers=2) as executor:
        futures = []
        for i in range(9):
            future = executor.submit(error_task, i)
            futures.append(future)
        
        # Handle results with error checking
        successful_results = []
        failed_tasks = []
        
        for future in as_completed(futures):
            try:
                result = future.result()
                successful_results.append(result)
                print(f"✓ {result}")
            except Exception as e:
                failed_tasks.append(str(e))
                print(f"✗ Exception: {e}")
    
    print(f"Successful: {len(successful_results)}")
    print(f"Failed: {len(failed_tasks)}")
    print()

# Example 5: Callbacks and custom result processing

# Move functions to module level to make them picklable
def task_with_callback(task_id):
    """Task that returns a dictionary - defined at module level"""
    sleep(random())
    return {
        'task_id': task_id,
        'result': task_id * 10,
        'process_id': os.getpid(),
        'timestamp': time()
    }

def process_result(future):
    """Callback function to process results - defined at module level"""
    try:
        result = future.result()
        print(f"Callback: Task {result['task_id']} = {result['result']} "
              f"(PID: {result['process_id']})")
    except Exception as e:
        print(f"Callback: Error processing result: {e}")

def callback_example():
    """Demonstrate using callbacks with ProcessExecutor"""
    print("=== ProcessExecutor Callback Example ===")
    
    with ProcessPoolExecutor(max_workers=3) as executor:
        futures = []
        for i in range(5):
            future = executor.submit(task_with_callback, i)
            future.add_done_callback(process_result)
            futures.append(future)
        
        # Wait for all to complete
        for future in futures:
            future.result()
    
    print()

# Example 6: Chunked processing with map()
def chunked_task(chunk):
    """Process a chunk of data"""
    results = []
    for item in chunk:
        # Simulate processing
        sleep(0.01)
        results.append(item * 2)
    return results

def process_executor_chunked():
    """Demonstrate chunked processing"""
    print("=== ProcessExecutor Chunked Processing Example ===")
    
    # Large dataset
    data = list(range(1000))
    chunk_size = 100
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    
    print(f"Processing {len(data)} items in {len(chunks)} chunks...")
    
    start_time = time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        chunk_results = list(executor.map(chunked_task, chunks))
    
    # Flatten results
    all_results = []
    for chunk_result in chunk_results:
        all_results.extend(chunk_result)
    
    end_time = time()
    print(f"Processed {len(all_results)} items in {end_time - start_time:.2f}s")
    print(f"Sample results: {all_results[:10]}...")
    print()

# Example 7: Resource management and cleanup
class ResourceManager:
    """Example of managing resources across processes"""
    
    def __init__(self):
        self.resource_id = randint(1000, 9999)
    
    def __enter__(self):
        print(f"Initializing resource {self.resource_id}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Cleaning up resource {self.resource_id}")

def resource_task(task_id, resource_id):
    """Task that uses a resource"""
    sleep(random())
    return f"Task {task_id} used resource {resource_id}"

def process_executor_resource_management():
    """Demonstrate resource management"""
    print("=== ProcessExecutor Resource Management Example ===")
    
    with ResourceManager() as resource:
        with ProcessPoolExecutor(max_workers=2) as executor:
            futures = []
            for i in range(4):
                future = executor.submit(resource_task, i, resource.resource_id)
                futures.append(future)
            
            results = [future.result() for future in futures]
            
            for result in results:
                print(f"  {result}")
    
    print()

# Example 8: Performance comparison
def cpu_bound_task(n):
    """CPU-bound task for performance testing"""
    result = 0
    for i in range(n):
        result += i * i
    return result

def performance_comparison():
    """Compare sequential vs parallel processing"""
    print("=== ProcessExecutor Performance Comparison ===")
    
    # Test data
    test_data = [1000000] * 4  # 4 tasks, each doing 1M calculations
    
    # Sequential processing
    print("Sequential processing...")
    start_time = time()
    sequential_results = [cpu_bound_task(n) for n in test_data]
    sequential_time = time() - start_time
    print(f"Sequential time: {sequential_time:.2f}s")
    
    # Parallel processing
    print("Parallel processing...")
    start_time = time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        parallel_results = list(executor.map(cpu_bound_task, test_data))
    parallel_time = time() - start_time
    print(f"Parallel time: {parallel_time:.2f}s")
    
    # Calculate speedup
    speedup = sequential_time / parallel_time
    print(f"Speedup: {speedup:.2f}x")
    print(f"Results match: {sequential_results == parallel_results}")
    print()

# Example 9: Advanced: Custom ProcessPoolExecutor
class CustomProcessPoolExecutor(ProcessPoolExecutor):
    """Custom ProcessPoolExecutor with additional features"""
    
    def __init__(self, max_workers=None, **kwargs):
        super().__init__(max_workers=max_workers, **kwargs)
        self.completed_tasks = 0
        self.failed_tasks = 0
    
    def submit(self, fn, *args, **kwargs):
        """Override submit to add tracking"""
        future = super().submit(fn, *args, **kwargs)
        
        def callback(fut):
            try:
                fut.result()
                self.completed_tasks += 1
            except Exception:
                self.failed_tasks += 1
        
        future.add_done_callback(callback)
        return future
    
    def get_stats(self):
        """Get execution statistics"""
        return {
            'completed': self.completed_tasks,
            'failed': self.failed_tasks,
            'total': self.completed_tasks + self.failed_tasks
        }

def mixed_task(task_id):
    """Task that sometimes fails"""
    sleep(random())
    if task_id % 4 == 0:
        raise RuntimeError(f"Task {task_id} failed")
    return f"Task {task_id} succeeded"
    
def custom_executor_example():
    """Demonstrate custom ProcessPoolExecutor"""
    print("=== Custom ProcessPoolExecutor Example ===")
    
    with CustomProcessPoolExecutor(max_workers=3) as executor:
        futures = []
        for i in range(8):
            future = executor.submit(mixed_task, i)
            futures.append(future)
        
        # Wait for all to complete
        for future in futures:
            try:
                result = future.result()
                print(f"  {result}")
            except Exception as e:
                print(f"  Error: {e}")
        
        # Get statistics
        stats = executor.get_stats()
        print(f"Statistics: {stats}")
    print()

# Main execution
if __name__ == '__main__':
    print("ProcessExecutor Examples")
    print("=" * 50)
    
    # Run all examples
    basic_process_executor()
    process_executor_map()
    process_executor_as_completed()
    process_executor_error_handling()
    callback_example()
    process_executor_chunked()
    process_executor_resource_management()
    performance_comparison()
    custom_executor_example()
    
    print("All examples completed!") 
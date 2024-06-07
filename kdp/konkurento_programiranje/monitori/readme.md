<div align="justify">

# Monitors in Concurrent Programming

## Monitor Structure

A monitor is a synchronization construct that allows threads to have both mutual exclusion and the ability to wait (block) for a certain condition to become true. Monitors encapsulate shared variables, operations, and the synchronization that governs access to these variables.

Here's an example of a simple monitor:

```cpp
monitor MyMonitor {
    int p1, p2;       // Permanent variables, their value does not change outside methods
    cond cond1, cond2; // Condition variables
    
    void method() {
        int lp1, lp2; // Local variables
    }
}
```

### Key Points
- **Separation of Code**: Monitors separate synchronization code from ordinary sequential code, making it easier to reason about synchronization.
- **Non-busy Waiting**: A method that involves busy waiting should never enter a monitor procedure.

## Methods on Condition Variables

Condition variables in monitors provide a way for threads to block and be woken up. The following methods are used to manipulate condition variables:

### `cond.wait()`
- **Unconditional Blocking**: The calling thread is blocked until another thread signals it.

### `cond.signal()`
- **No Waiting Thread**: Does nothing if there are no waiting threads.
- **With Waiting Threads**:
  - **SW (Signal and Wait)**: Transfers the right of access to the woken thread.
  - **SUW (Signal and Urgent Wait)**: Transfers the right of access to the woken thread and guarantees that the signaling process will execute immediately after the woken thread.
  - **SC (Signal and Continue)**: The signaling thread continues its execution.

- **Last Instruction**: If `cond.signal()` is the last instruction, under SW and SUW disciplines, the signaling process does not go into the `EntryQueue`.

### `cond.signalAll()`
- **Wake All**: Wakes all processes waiting on this condition.
- **Discipline**: Only applicable with SC discipline.

### `cond.wait(prioritet)`
- **Priority-based Waiting**: The thread is blocked, and a priority is assigned where a lower number indicates higher priority.

### `cond.minrank()`
- **Get Highest Priority**: Returns the highest priority in the waiting queue.

### `cond.empty()`
- **Check if Queue is Empty**: Returns `true` if the queue is empty.

### `cond.queue()`
- **Check if Queue is Not Empty**: Returns `true` if the queue is not empty.

## Summary

Monitors provide a high-level abstraction for thread synchronization, hiding the complex details of the lock and condition variables. By using monitors, you can ensure that your concurrent program is easier to write, understand, and maintain.

Here's a more detailed example of a monitor with methods for synchronization:

```cpp
monitor MyMonitor {
    int p1, p2;       // Permanent variables
    cond cond1, cond2; // Condition variables
    
    void method1() {
        int lp1, lp2; // Local variables
        // Perform operations
        if (/* some condition */) {
            cond1.wait(); // Wait for cond1 to be signaled
        }
        // Continue operations
    }
    
    void method2() {
        // Perform operations
        if (/* some condition */) {
            cond1.signal(); // Signal cond1
        }
        // Continue operations
    }
}
```


This monitor ensures that `method1` and `method2` can safely access and modify the shared variables `p1` and `p2` while providing mechanisms for threads to wait and signal each other based on certain conditions.

# Disciplines 

### 1. **SW (Signal and Wait)**
In the SW discipline, when a thread issues a `signal` on a condition variable, it immediately transfers control to the waiting thread. The signaling thread then waits for its turn to continue execution. This ensures that the waiting thread runs immediately, giving it higher priority.

- **Behavior**: 
  - The signaling thread transfers control to the signaled thread.
  - The signaling thread then waits until the signaled thread releases the monitor.
  
- **Use Case**: 
  - Suitable in scenarios where it is crucial for the waiting thread to run as soon as possible after being signaled, without being preempted by other threads.

### 2. **SUW (Signal and Urgent Wait)**
SUW is similar to SW, with an additional guarantee. When a thread issues a `signal`, it not only transfers control to the waiting thread but also ensures that the signaling thread will continue immediately after the signaled thread finishes. This gives the signaling thread a higher priority than any other threads that may attempt to enter the monitor.

- **Behavior**:
  - The signaling thread transfers control to the signaled thread.
  - The signaling thread gets higher priority to continue execution immediately after the signaled thread completes its work.

- **Use Case**:
  - Useful in real-time systems or scenarios where both the waiting thread and the signaling thread need to run in quick succession without being interrupted by other threads.

### 3. **SC (Signal and Continue)**
In the SC discipline, when a thread issues a `signal`, it continues its execution immediately. The signaled thread is awakened but will only execute after the signaling thread leaves the monitor. This approach can prevent the monitor from being handed off immediately, allowing the signaling thread to finish its current operations.

- **Behavior**:
  - The signaling thread continues its execution after issuing the `signal`.
  - The signaled thread waits until the monitor is free to resume its execution.

- **Use Case**:
  - Suitable in situations where the signaling thread has critical work to complete and should not be interrupted immediately after issuing a signal. It ensures that the signaling thread's critical section is completed before the waiting thread can proceed.

### Practical Example:
Let's put these disciplines into a practical context using a simple producer-consumer problem:

#### SW Example:
```cpp
monitor Buffer {
    int items = 0;
    cond notEmpty, notFull;

    void produce() {
        if (items == MAX_ITEMS) {
            notFull.wait(); // Wait if buffer is full
        }
        // Produce an item
        items++;
        notEmpty.signal(); // Signal that buffer is not empty
    }

    void consume() {
        if (items == 0) {
            notEmpty.wait(); // Wait if buffer is empty
        }
        // Consume an item
        items--;
        notFull.signal(); // Signal that buffer is not full
    }
}
```

In this SW example, when `produce()` signals `notEmpty`, the consumer waiting on `notEmpty` immediately gets to run.

#### SUW Example:
Similar to SW, but with a guarantee that the producer will immediately continue after the consumer if `notEmpty.signal()` is the last operation in `produce()`.

#### SC Example:
```cpp
monitor Buffer {
    int items = 0;
    cond notEmpty, notFull;

    void produce() {
        if (items == MAX_ITEMS) {
            notFull.wait(); // Wait if buffer is full
        }
        // Produce an item
        items++;
        notEmpty.signal(); // Signal that buffer is not empty
    }

    void consume() {
        if (items == 0) {
            notEmpty.wait(); // Wait if buffer is empty
        }
        // Consume an item
        items--;
        notFull.signal(); // Signal that buffer is not full
    }
}
```

In this SC example, after `produce()` signals `notEmpty`, it continues execution until it exits the monitor. The consumer waiting on `notEmpty` will only run after `produce()` finishes.

### Summary:
Each discipline provides different guarantees about the execution order of the threads. Choosing the right discipline depends on the specific requirements of the concurrency problem you are solving, such as ensuring fairness, preventing starvation, or optimizing for performance and responsiveness.

</div>
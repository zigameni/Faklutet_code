# CLH Algorithm

 The CLH (Craig, Landin, and Hagersten) algorithm is a lock-based algorithm used for managing access to critical sections in concurrent programming. It is designed to provide a scalable and efficient solution for mutual exclusion, ensuring that only one process can enter the critical section at a time. The algorithm relies on a queue of nodes where each node represents a process waiting to enter the critical section.

### Detailed Explanation of CLH Algorithm

1. **Queue of Nodes:**
   - The CLH algorithm uses a linked list of nodes (queue) where each node represents a process waiting to enter the critical section.

2. **Lock Acquisition:**
   - Each process creates a new node and links it to the end of the queue by atomically updating the `tail` pointer. The process then waits until its predecessor's node is unlocked.

3. **Lock Release:**
   - When a process leaves the critical section, it unlocks its own node, allowing the next process in the queue to proceed.

4. **Scalability:**
   - The CLH lock is highly scalable because each process spins on its local node, reducing contention on shared variables.

By using the CLH algorithm, processes can efficiently manage access to the critical section in a concurrent environment, ensuring mutual exclusion and minimizing contention.

### CLH Algorithm – Coarse Grain

#### Pseudo Code

```cpp
struct Node {
    bool locked;
};

Node tail = {false};

void CS(int i) {
    while (true) {
        Node prev, node = {true}; // Entry protocol
        prev = tail;
        tail = node;
        while (prev.locked); // Wait until the previous node is unlocked
        // Critical section
        node.locked = false; // Exit protocol
        // Non-critical section
    }
}
```

#### Explanation

1. **Initialization:**
   - `Node tail = {false}`: A shared `tail` node, initially unlocked (`false`).

2. **Process Structure:**
   - Each process `CS[i]` repeatedly executes a loop.

3. **Entry Protocol:**
   - `Node prev, node = {true}`: Create a new node `node` and set its `locked` status to `true`, indicating the process wants to enter the critical section.
   - `prev = tail; tail = node;`: Atomically set the current `tail` to the new node and get the previous `tail` node in `prev`.
   - `while (prev.locked);`: Wait (busy-wait) until the previous node is unlocked.

4. **Critical Section:**
   - The process enters its critical section.

5. **Exit Protocol:**
   - `node.locked = false;`: Unlock the current node, signaling that the process is leaving the critical section.

6. **Non-Critical Section:**
   - The process executes the non-critical section.

### CLH Algorithm – Fine Grain

#### Pseudo Code

```cpp
struct Node {
    bool locked;
};

Node tail = {false};

void CS(int i) {
    while (true) {
        Node prev, node = {true}; // Entry protocol
        prev = GS(tail, node); // Use Get and Set operation
        while (prev.locked); // Wait until the previous node is unlocked
        // Critical section
        node.locked = false; // Exit protocol
        // Non-critical section
    }
}
```

#### Explanation

1. **Initialization:**
   - Similar to the coarse grain version with `Node tail = {false}`.

2. **Process Structure:**
   - Each process `CS[i]` repeatedly executes a loop.

3. **Entry Protocol:**
   - `Node prev, node = {true}`: Create a new node `node` and set its `locked` status to `true`.
   - `prev = GS(tail, node);`: Use the atomic Get-and-Set operation to set the current `tail` to the new node and return the previous `tail` node in `prev`.
   - `while (prev.locked);`: Wait until the previous node is unlocked.

4. **Critical Section:**
   - The process enters its critical section.

5. **Exit Protocol:**
   - `node.locked = false;`: Unlock the current node.

6. **Non-Critical Section:**
   - The process executes the non-critical section.

### Get and Set (GS) Operation

The Get-and-Set operation is a special atomic instruction used to update variables:

```cpp
int GS(var, new) {
    int tmp = var;
    var = new;
    return tmp;
}
```

- **Purpose:** Atomically fetch the old value of a variable and set it to a new value.
- **Usage in CLH Algorithm:**
  - `prev = GS(tail, node);`: Atomically update `tail` to point to the new `node` and retrieve the old `tail` in `prev`.


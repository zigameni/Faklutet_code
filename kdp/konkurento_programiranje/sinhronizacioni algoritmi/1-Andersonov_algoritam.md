## Andersen's Algorithm – Coarse Grain

```cpp
int slot = 0, flag[1:n] = ([n] false); 
flag[1] = true;

process CS[i = 1 to n] {
    int myslot;
    while (true) {
        <myslot = slot mod n + 1; slot = slot + 1;>
        <await(flag[myslot])>
        critical section;
        <flag[myslot] = false;
        flag[myslot mod n + 1] = true;>
        noncritical section
    }
}
```

## Andersen's Algorithm – Fine Grain

```cpp
int slot = 0, flag[1:n] = ([n] false); 
flag[1] = true;

process CS[i = 1 to n] {
    int myslot;
    while (true) {
        myslot = FA(slot, 1) mod n + 1; /*entry protocol*/
        while (!flag[myslot]) skip;
        critical section;
        flag[myslot] = false; /* exit protocol */
        flag[myslot mod n + 1] = true;
        noncritical section
    }
}
```

### Explanation of Andersen's Algorithm

**Coarse Grain Version:**

1. **Initialization:**
    - `int slot = 0`: A shared integer `slot` that keeps track of the current slot.
    - `flag[1:n] = ([n] false)`: An array `flag` of size `n` initialized to `false`.
    - `flag[1] = true`: Set the first flag to `true`.

2. **Process Structure:**
    - Each process `CS[i]` (where `i` ranges from 1 to `n`) repeatedly executes a loop.
    - **Entry Protocol:**
        - `myslot = slot mod n + 1`: Calculate the slot for the current process.
        - `slot = slot + 1`: Increment the slot.
        - `await(flag[myslot])`: Wait until the flag for `myslot` is `true`.
    - **Critical Section:**
        - The process enters its critical section.
    - **Exit Protocol:**
        - `flag[myslot] = false`: Set the current flag to `false`.
        - `flag[myslot mod n + 1] = true`: Set the next slot's flag to `true`.
    - **Non-Critical Section:**
        - The process then executes the non-critical section.

**Fine Grain Version:**

1. **Initialization:**
    - Similar to the coarse grain version, with `slot` and `flag` array initialization.

2. **Process Structure:**
    - Each process `CS[i]` (where `i` ranges from 1 to `n`) repeatedly executes a loop.
    - **Entry Protocol:**
        - `myslot = FA(slot, 1) mod n + 1`: Use the Fetch-and-Add (`FA`) atomic operation to get the slot and increment it by 1.
        - `while (!flag[myslot]) skip;`: Wait (busy-wait) until the flag for `myslot` is `true`.
    - **Critical Section:**
        - The process enters its critical section.
    - **Exit Protocol:**
        - `flag[myslot] = false`: Set the current flag to `false`.
        - `flag[myslot mod n + 1] = true`: Set the next slot's flag to `true`.
    - **Non-Critical Section:**
        - The process then executes the non-critical section.

### Detailed Explanation:

1. **Slot Management:**
    - Both algorithms use a slot mechanism to manage access to the critical section. The `slot` variable is incremented to ensure that each process gets a turn to enter the critical section.

2. **Flag Array:**
    - The `flag` array is used to signal which process can enter the critical section. Only one `flag` will be `true` at any given time, corresponding to the process that is allowed to enter the critical section.

3. **Entry and Exit Protocols:**
    - In the coarse grain version, the entry protocol is a simple increment and modulo operation to determine the slot. The exit protocol involves setting the current flag to `false` and the next flag to `true`.
    - In the fine grain version, the entry protocol uses an atomic Fetch-and-Add operation to ensure that the slot increment operation is atomic, preventing race conditions. The exit protocol is similar to the coarse grain version.

4. **Synchronization:**
    - Both versions ensure mutual exclusion, meaning only one process can be in the critical section at a time. The flag mechanism and slot management ensure that processes enter the critical section in a controlled manner.

By using these mechanisms, Andersen's algorithm provides a structured way to manage process synchronization, ensuring that each process gets a fair turn to execute its critical section without interference from other processes.# Andersenov algoritam 


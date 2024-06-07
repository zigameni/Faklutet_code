# Tie breaker algoritam 

<div align="justify">

### Tie-breaker - coarse grain 

```cpp
bool in1 = false;
bool in2 = false;
int last = 1;

void worker1(){
    while(1){
        in1 = true; // I want to enter
        last=1;     // i am last to want to enter. 

        <await(!in2 && last==2);>
        // cs

        in1 = false;
        // non cs
    }
}

void worker2() {
    while(1) {
        in2 = true;
        last = 2;
        <await(!n1 && last==1);>
        // cs
        in2 = false; 
        // non cs
    }
}


```
### Tie-breaker - Fine grain


```cpp
bool in1 = false;
bool in2 = false;
int last = 1;

void worker1(){
    while(1){
        in1 = true; // I want to enter
        last=1;     // i am last to want to enter. 

        // <await(!in2 && last==2);>
        while(in2 && last!=2){ // busy wait}
        // cs

        in1 = false;
        // non cs
    }
}

void worker2() {
    while(1) {
        in2 = true;
        last = 2;
        // <await(!n1 && last==1);>
        while(in1 && last!=1) { // busy wait }
        // cs
        in2 = false; 
        // non cs
    }
}


```



# Tie breaker for N processess. 

Here is the translation of the provided text, formatted using GitHub Markdown and written as pseudo C++ code:

### Tie-Breaker for n Processes
- `n states` – which process moves to the next state is determined by the Tie-Breaker (Peterson’s) algorithm for two processes
- At most one process can pass through all n-1 states at a time
- Two integer arrays are introduced: `in[1:n]`, `last[1:n]`
- `in[i]` – the state process `CS[i]` is currently in
- `last[j]` – the process that last entered state `j`

### Tie-Breaker for n Processes
- Outer loop n-1 times
- Inner loop – `CS[i]` waits in the current state if there is a process in a higher or the same state and `CS[i]` was the last to enter state `j`
- If there is no process in a higher state waiting to enter the critical section or another process is entering state `j`, `CS[i]` can move to the next state
- At most n-1 processes can pass the first state, n-2 processes the second state, ..., one process the last state – Critical Section

### Pseudo C++ Code

```cpp
int in[n] = {0}, last[n] = {0};

void process(int i) {
    while (true) {
        // Entry protocol
        for (int j = 1; j < n; ++j) {
            in[i] = j;
            last[j] = i;
            for (int k = 1; k <= n; ++k) {
                if (i != k) { // the process does not compare itlsef to itslef
                    while (in[k] >= in[i] && last[j] == i) {
                        // Busy wait
                    }
                }
            }
        }

        // Critical section
        critical_section();

        // Exit protocol
        in[i] = 0;

        // Non-critical section
        non_critical_section();
    }
}

void critical_section() {
    // Code for critical section goes here
}

void non_critical_section() {
    // Code for non-critical section goes here
}
```

In this pseudo C++ code:
- `in` and `last` are arrays to track the states of the processes.
- The `process` function simulates each process's behavior.
- The outer loop runs `n-1` times, and the inner loop ensures that the current process waits if another process is in a higher or the same state and was the last to enter that state.
- The `critical_section` and `non_critical_section` functions are placeholders for the respective sections of the process.


For every state, we take the process through that state and set the last process to enter that state to the current process. This ensures that we keep track of which process was the last to attempt entry into each state. The process cannot proceed to the next state if there is another process in a higher or the same state, ensuring a strict ordering and preventing multiple processes from advancing simultaneously.

</div>
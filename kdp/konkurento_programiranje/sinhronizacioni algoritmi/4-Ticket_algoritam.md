## Ticket Algoritam

<div align="justify">
- Everyone attempting to enter the critical section first receives a ticket with a number in the order of arrival.
- Fair critical section
- One at a time in the order of arrival (ticket)
- Restaurant services – fair services

### Coarse grain resenje

```cpp
const int N = ...;

int index = 1;
int next = 1; 

// the queue, rounded
int turn[1:N] = ([N]0);

// podrzaumeva da i ide od 1 to N;
void worker(int i){
    <
        turn[id] = index;
        index = index + 1; 
    >

    <await(turn[id]==next);>
    // cs

    <next = next + 1;>
    // non cs
}

```
### Fine grain resenje

Fine grain resenje koristi specijalnu instrukciju `Fetch and add`. 

#####  Fetch and Add

- Special instruction for processors
- Incrementing a variable with a constant as an atomic action while returning the old value
```cpp
FA(var, incr):
    <int tmp = var; var = var + incr; return(tmp);>
```
- Use FA for <turn [i] = number; number = number + 1;>
- The rest is handled by AMOP because each process has its own turn[i], and incrementing next is at the end of the critical section – only one process modifies it at a time!

```cpp
// Example usage of FA for ticket algorithm
int number = 1, next = 1, turn[n] = {0};

void process(int i) {
    while (true) {
        // Entry section using Fetch and Add (FA)
        turn[i] = FA(number, 1);
        
        // Wait until it's this process's turn
        while (turn[i] != next) {
            // Busy wait
        }

        // Critical section
        critical_section();

        // Exit section
        next = next + 1;

        // Non-critical section
        non_critical_section();
    }
}

```


</div>
# Februar 2023, 1. zadatak

<div align="justify">

Fine grain `Ticket algoritam` realizovan pomoću `addAndGet` operacije. Ukoliko bi addAndGet operacija imala sledeći efekat: `addAndGet(var, incr) : < var = var + incr; return(var);`, da li je moguće napraviti Fine grain rešenje, polazeći od Coarse grain rešenja, i ako je moguće - napravite ga. Napisati i Coarse grain rešenje.


### Resenje

#### Coarse grain resenje

```cpp

// const int N = ...;
int ticket = 0;
int next = 0; 

void worker() {
    while(true){
        int myTicket = 0;
        < myTicket = ticket++; >
        < await(myTicket == next );>
        // cs

        next++;
        // non cs
    }
}

```

#### Fine grain resenje with addAndGet()

`addAndGet(var, incr) : < var = var + incr; return(var);`

```cpp

// const int N = ...;
int ticket = 0;
int next = 0; 

void worker() {
    while(true){
        int myTicket = 0;
        myTicket = addAndGet(ticket, 1) - 1;

        while(ticket != myTicket) { }
        // cs

        next++;
        // non cs
    }
}

```


</div>
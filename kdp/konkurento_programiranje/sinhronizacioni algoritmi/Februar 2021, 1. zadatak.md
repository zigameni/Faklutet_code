## Februar 2021, 1. zadatak
<div align="justify">

#### Postavka

Napisati i objasnite test and test and set rešenje za kritičnu sekciju. Ukoliko bi umesto TS(var) postojala operacija SWAP koja bi nedeljivo obavljala zamenu vrednosti dva operanda (SWAP(var1, var2) : < temp = var1; var1 = var2; var2 = temp; >), da li je moguće napraviti Fine grain rešenje i ako je moguće – napravite ga.

#### Resenje

`Test and Set` je specialna instrukcija za procesore, `Atomska Akcija` uzme staru boolean vrednost i vraca je, ujedno nedeljivo postavlja vrednost na true.

```cpp

bool TS(bool lock){
    <
     bool initial = lock;
     lock = true;
     return initial;
    >
}

```
##### Test and set, Kriticna sekcija 

```cpp

void worker(){
    while(1){
        while(TS(lock))skip();

        // Kriticna sekcija 

        lock = false;

        // no cs
    }
}
```

##### SWAP Kritica sekcija
`SWAP`(var1, var2): < temp = var1; var1 = var2; var2=temp; > 
```cpp

bool lock = false;

void worker () {
    while(true){
        bool initialLock = true;
        while(lock == true)skip;
        swap(lock, initialLock);
        while(initialLock==true){
            while(lock==true)skip();
        }

        // Kriticna sekcija 
        lock = false; 

        // Non critical section. 
    }

}





```

</div>
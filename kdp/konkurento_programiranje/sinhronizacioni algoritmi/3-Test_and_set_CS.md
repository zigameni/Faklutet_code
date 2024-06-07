# Test and set 

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
### Test and set, Kriticna sekcija 

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
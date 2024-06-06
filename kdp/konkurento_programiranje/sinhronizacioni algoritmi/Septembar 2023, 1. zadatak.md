## Septembar 2023, 1. zadatak

 Napisati i objasniti CLH algoritam za kritičnu sekciju (coarse grain). Realizovati (fine grain) verziju algoritma ukoliko bi na datom procesoru postojala operacija SWAP koja bi nedeljivo obavljala zamenu verdnosti dva operanda (SWAP(var1, var2): <temp=var1; var1=var2; var2=temp;>). Objasniti zašto je to pravična kritična sekcija.

### Resenje

```cpp
Node tail = {false};

void worker () {

    while(1) {

        <Node prev, node = {true};>
        <prev = tail;>
        <tail = node>

        while(prev.locked) skip();

        // CS

        node.locked = false;
    }
}

// the algorithm uses a linked list to order the processes as they come. 
```

### Fine grain with swap
`SWAP(var1, var2)`: <temp=var1; var1=var2; var2=temp;>

```cpp
struct Node {
    bool locked;
    Node(){
        locked = true;
    }
}
Node* tail = nullptr;

void worker(){
    while(1) {
        Node*node = new Node();
        Node* prev = node;
        SWAP(prev, tail);
        while(prev != nullptr && prev->locked)skip;

        // cs

        node.locked = false;

        // non cs
    }
}



```


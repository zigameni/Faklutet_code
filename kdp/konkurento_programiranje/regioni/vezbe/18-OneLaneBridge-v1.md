# One lane bridge problem 
    Cars coming from the north and south must cross a river via a bridge. Unfortunately, there is only one lane on the bridge. This means that at any given time, one or more cars from the same direction can cross the bridge (but not from the opposite direction simultaneously). Write an algorithm for cars coming from the north and cars coming from the south that arrive at the bridge, cross it, and leave on the other side.

### V1 ima izgladnjivanje 

```cpp
struct Bridge{
    int N = 0; // Number of cars comming from the North
    int S = 0; // Numbe rof cars from the south
};

Bridge bridge;

void north(){
    // Regioni koriste struct da bi mogli da manipulisu nekoliko podataka

    // waiting to cross the bridge 
    region(bridge){
        // wait until no cars are comming from the south. 
        await(S==0);
        N++;        
    }

    cross();
    
    region(bridge){
        // get of the bridge
        N--;
    }
}

void south(){
    // waiting to cross the bridge 
    region(bridge){
        // wait until there are no cars comming from the north
        await(N==0);
        s++;
    }
    cross();
    
    // leving the bridge
    region(bridge){
        S--;
    }
}

// The problem with this solution is that cars from one side might not even get a chance to cross if cars from the other side just keep comming. 

```
// One lane bridge problem 
// Cars coming from the north and south must cross a river via a bridge. Unfortunately, there is only one lane on the bridge. This means that at any given time, one or more cars from the same direction can cross the bridge (but not from the opposite direction simultaneously). Write an algorithm for cars coming from the north and cars coming from the south that arrive at the bridge, cross it, and leave on the other side.

// V2 nema izgladnjivanje

struct Bridge{
    int N = 0; // Number of cars comming from the North
    int S = 0; // Numbe rof cars from the south
    int waitN = 0, waitS = 0;  // number of cars waiting to cross
    int crossN = 0, crossS = 0; // number of cars that are currently crossing, or have crossed. 

};

Bridge bridge;

void north(){
    // Regioni koriste struct da bi mogli da manipulisu nekoliko podataka

    // waiting to cross the bridge 
    region(bridge){
        waitN++;     
        await(S==0 && crossN<K);
        waitN--;
        
        N++;    
        if(waitS>0){
            crossN++; // let car cross
        }
    }
    cross();
    region(bridge){
        N--;
        if(n==0){
            crossS=0;
        }
    }
}

void south(){
    // waiting to cross the bridge 
    region(bridge){
        waitS++; // cars wating to cross
        await(N==0 && crossS<K);
        waitS--;
        S++;

        if(waitN > 0){
            cross++;
        }        
    }
    cross();
    // leving the bridge
    region(bridge){
        
        s--;
        if(s==0){
            crossN = 0; //Which means they can cross. 
        }
    }
}

// The problem with this solution is that cars from one side might not even get a chance to cross if cars from the other side just keep comming. 

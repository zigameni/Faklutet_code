# Regioni uslovna sisnhronizacija
    Producer-consumer problem.

```cpp
const int N = 100;
struct Point {
    int x = 0;
    int y = 0; 
    bool full = true;
};

Point point; 

void makePoints(){
    for (int i = 1; i <= N; i++) {
        region (point){
            await(!full);
            x = i;
            y = i+1;
            full = true;
        }
    }   
}


void printPoints(){
    for (int i = 0; i <= N; i++)
    {
        await(full);
        print(x);
        print(y);
        full = false;
    }
    
}

```
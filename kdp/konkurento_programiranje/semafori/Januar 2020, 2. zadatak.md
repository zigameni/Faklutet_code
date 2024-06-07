# Januar 2020, 2. zadatak 
    Problem Putovanja liftom

<div align="justify">
Koristeći semafore napisati program koji rešava problem putovanja liftom. Putnik poziva lift sa proizvoljnog sprata. Kada lift stigne na neki sprat svi putnici koji su izrazili želju da siđu na tom spratu obavezno izađu. Nakon izlaska putnika svi putnici koji su čekali na ulazak uđu u lift i kažu na koji sprat žele da pređu. Tek kada se svi izjasne lift prelazi dalje. Lift redom obilazi spratove i staje samo na one gde ima putnika koji ulaze ili izlaze. Može se pretpostaviti da postoji N spratova.


### Resenje

```cpp

struct Floor {
    list<sem*> peopleEntering;
    list<sem*> peopleExiting;
    sem mutexEntering = 1;
    sem mutexExiting = 1;
};

const int N = 10; // Number of floors
Floor floors[N];
sem liftSem = 0;

void person(){
    sem personSem = 0;

    // get the current floor 
    int currentFloorIndex = rand()%N;
    
    while(1){
        // get the next floor
        int nextFloorIndex = rand()%N;
        Floor& cuurentFloor = floors[currentFloorIndex];
        Floor& nextFloor = floors[nextFloorIndex];

        currentFloor.mutexEntering.wait(); // controls access to list peopleEntering

        // add person to list of wating for lift on the current floor 

        // unlock access to the list. 

        // let the person wait until he gets notified that it can get intot he lift. 
        personSem.wait();

        // Улазимо у лифт и бирамо на којем спрату стајемо
        nextFloor.mutexExiting.wait();
        nextFloor.peopleExiting.push_back(&personSem);
        nextFloor.mutexExiting.signal();

        liftSem.signal();

        




    }
}


void lift(){
    int currentFloorIndex = 0;
    bool goingUp = true;
    while(1){

        if(goingUp){
            if(++currentFloorIndex == N-1){
                goingUp = false;
            }
        }else {
            if(--currentFLoorIndex == 0){
                goingUp = true;
            }
        }

        Floor& floor = floors[currentFLoorIndex];

        // first needs to let people off, than get the others on. 

        int countPeopleExiting = floor.peopleExiting.size();
        floor.mutexEntering.wait();
        int countPeopleEntering = floor.peopleEntering.size();

        if(countPeopleEnetring == 0 && countPeopleExiting == 0) {
            // ne stajemo na ovom spratu.
            floor.mutexEntering.signal();

        }



    }
}
```



</div>
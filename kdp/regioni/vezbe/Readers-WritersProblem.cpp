// Readers-Writers Problem 


void read();
void write();

struct RW {
    int writers = 0;
    int readers = 0; 
};

RW rw;

void reader(){

    while ( 1 ) {
        region( rw ) {
            await(w == 0);
            r++;
        }
        read();

        region( RW ) {
            r--;
        }
    }
}


void writer(){
    while(1){
        region(RW) {
            await(w==0); // we check so that there are no other readers
            w++;
            wait(r==0);  // we check so that there are no other writers.   
        }
        write();

        region(rw){
            w--;
        }
    }
}

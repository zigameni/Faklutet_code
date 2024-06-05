// Readers-Writers, FIFO

struct RW 
{
    int W=0, R=0;
    int ticket = 0;
    int next = 0;
};

RW rw;

void reader() {

    int myTicket;
    region(rw){
        
        // get a ticket 
        // check if it is my tickets turn 
        // inc the ticket by one, auto
        // inc the nr of readers
        myTicket = ticket++;
        wait(w==0 && myTicket == next);
        next++;
        r++;
    }

    read();
    region(rw){
        r--;
    }

}
void writer() {
    // same principle 
    int myTicket;
    region(rw) {
        myTicket = ticket++;
        await(w==0 && r==0 & myTicket == next);
        next++;
        w++;
    }

    write();
    region(rw){
        w--;
    }

}
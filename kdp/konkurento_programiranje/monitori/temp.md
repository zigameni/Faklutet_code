
# Producer consumer porblem with Singnal and Wait discipline

```cpp

monitor ProducerConsumer {
    T buffer[N];
    int head = 0;
    int tail = 0; 
    int size = 0;   
    cond not_full;  // conditional variable to manage producer wait 
    cond not_empty; // conditional variable to manage consumer wait. 

    void produce(T item) {
        // if the buffer is full the procuder waits
        if(size == N){
            not_full.wait(); // producer wait
        }

        buffer[tail] = item;

        tail = (tail + 1) % N;

        size++;

        if(not_empty.queue()){
            not_empty.signal();
        }
    }


    T consume(){
        // is the queue mpty?
        if(size == 0){
            not_empty.wait();
        }

        T item = buffer[head];
        head = (head+1) % N;

        size = --;
        if(not_full.queue()){
            not_full.signal();
        }
        return iteml;
    }
}

```

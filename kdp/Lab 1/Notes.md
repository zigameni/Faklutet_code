# konkuretno Programiranje (lab 1)

```Java
public class MyThread extends Thread{
    public void run(){
        ...
    }
}

// Instanciranje 
myThread = new MyThread();

myThread.start();

// Second method for thread, Runnable interface

public class MyThread implements Runnable{
    public void run(){
        ...
    }
}

// Instanciranje 
Thread myThread = new Thread(new MyThread(...));

myThread.start();

// Cekanje da se izvrsavnje niti zavrsi:
myThread.join();

// Prepustanje prava izvrsavanja drugoj niti 
myThread.yield();

// Suspendovanje izvrsavanja niti na vremenski period t;
myThread.sleep(t);


```
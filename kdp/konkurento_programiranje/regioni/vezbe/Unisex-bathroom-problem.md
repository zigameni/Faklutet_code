// Unisex bathroom problem
// There is a toilet with a capacity of N (N > 1) that can be used by both women and men, such that women and men cannot be in the toilet at the same time. Write a program for women and men who come to the toilet, use it, and leave it using conditional critical regions. Avoid starvation.


struct WC {
    int cntM = 0, cntW = 0;
    int waitingM = 0, waitingW = 0;
    int turn = 0; // 0 - niko nema prednost, 1 - muskaraci, 2 - zena
};

WC wc;

void women(){
    // enter wc,
    region(wc) {
        waitingW++;
        await(cntM == 0 && turn != 1 && cntW<N);
        waitingW--;
        cntW++;
        if(watingM > 0) {
            turn = 1;
        }
    }

    useToilet();

    // izlazak iz vc
    region(wc) {
        cntW--;
        if(cntW==0 && watingM == 0){
            turn = 0;
        }
    }
}

void men(){

    region(wc) {
        watingM ++;
        await(cntW==0 && turn != 2 && cntM<N);
        watingM--;
        cntM++;
        if(watingW>0){
            turn = 2;
        }

        useToalet();

        region(wc) {
            cntM--;
            if(watingW == 0 && cntM==0){
                turn = 0;
            }
        }
    }
}
// Cigarette smokers problem

struct Smokers
{
    bool paper = false;
    bool matches = false;
    bool tobacco = false;
    bool next = false; 
};

Smokers smokers;

void agent(){
    while(1) {
        int i = random(0, 3);
        region(smokers){
            switch(i){
                case: 0:
                    tobacoo = true;
                    matches = true; 
                 break;
                case: 1:
                    tobacoo = true;
                    paper = true;
                 break;
                case: 2:
                    paper = true;
                    matches = true;
                 break;
            }
            await(next);
            next = false;
        }
        switch()

    }
}


void smoker_m(){
    while (1)
    {
        region(smokers) {
            await(paper && tobacco);
            paper = false;
            tobaco = false;
        }
        smoke();
        region(smokers) {
            next = true;
        }
    }
    
}


void smoker_p(){
while (1)
    {
        region(smokers) {
            await(tobacco && matches);
            tobacco = false;
            matches = false;
        }
        smoke();
        region(smokers) {
            next = true;
        }
    }

}

void smoker_t() {
while (1)
    {
        region(smokers) {
            await(paper && matches);
            paper = false;
            matches = false;
        }
        smoke();
        region(smokers) {
            next = true;
        }
    }

}
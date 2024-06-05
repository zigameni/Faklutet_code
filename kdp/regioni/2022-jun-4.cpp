// Трајект за превоз аутомобила, камиона и аутобуса превози возила са обале на обалу. Трајект поседује N позиција које су линеарно постављене једна иза друге. Камион заузима три, аутобус две, а аутомобил једну позицију. Возила чекају на трајект у реду и на њега улазе једно по једно по редоследу у којем чекају у реду, док на трајекту има места. Када наредно возило у реду за трајект нема места да се укрца или када је трајект пун, трајект започиње превоз возила на другу обалу. На другој обали возила се искрцавају у редоследу супротном од редоследа у којем су се укрцала. Када се сва возила искрцају, празан трајект се враћа на почетну обалу. Користећи регионе написати програм који решава овај проблем.


const int N = 100;

// kamion  - 3 pozicije
// autobus - 2 pozicije
// auto    - 1 pozicija

struct Trajekt {
    int cap = N;
    int current = 0, next=0, ticketIn = 0, ticketOut=0;
    bool getOn = false, getOff = false;
};

Trajekt t;

void cars (int space) {
    int myTicketIn, myTicketOut;

    region(t){
        myTicketIn = t.ticketIn ++;
        // Ako idemo po redu onda koristimo ticket.
        await(t.getOn && t.ticketIn == myTicketIn);

        // check if there is space
        if(t.cap -t.curr <space){
            // there is no space
            t.getOn = false;
            await(t.getOn); // There is no space so now we have to wait.
        }
        t.current += space;
        myTicketOut = ++t.ticketOut;
        t.next++;

        if(t.current == t.cap){
            t.getOn = false;
        }

        // the ferry travels to the other island.
        region(t){
            await(t.getOff && myTicketOut == t.ticketOut);

            if(--t.ticketOut == 0){
                // if i am the last one getting off
                t.getOff = false;
            }
        }
    }
}



void tajekt () {
    while(1){
        region(t){
            t.getOn = true;
            await(!t.getOn);
        }
        // travel to the other island
        region(t){
            t.getOff = true;
            await(!t.getOff);
        }

    }
}

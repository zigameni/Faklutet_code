// Проблем вожње аутобусом (The bus problem). Путници долазе на аутобуску станицу и чекају први аутобус који наиђе. Аутобус креће са станице када сви путници који су били на станици у тренутку доласка аутобуса провере да ли могу да уђу и уђу уколико има места. Путници се изјашњавају на којој станици ће изаћи из аутобуса. Капацитет аутобуса је K места. Путници који су дошли док је аутобус био на станици чекају на следећи аутобус. Постоје M аутобуса који саобраћају између N станица. Користећи условне критичне регионе написати програм за путнике и аутобусе.

const int K = 50; // kapacitet autobuza.
const int M = 5; // broj autobuza.
const int N = 60; // broj stanica.

// odrejduju sa koje stanice na koju stanicu ce ili putnici.
// podrazumeva se da jedan putnik nece ili sa jedna na tu istu stanicu.

int getStationIdFrom();
int getStationIdTo();

struct Station {
    // broj putnika koji cekaju
    int numPassangersEntering = 0;

    int passangersChecking=0;

    // broj putnika koji su vec u autobusu
    int busPassangers = 0;
    // redosled dolaska autobuza na stanici.
    int currTicket = 0;
    int nextTicket = 0;

    // Autobus koji je trenutno na stanici.
    int busId = -1;

    // broj putnika koji treba da izadju na stanici
    // iz sledeceg autobusa.
    int passangersExiting[M] = {0};
};

Station stations[N];



void bus(int busId){
    int stationId = 0;
    int numberOfPassangers = 0;

    while(true){
        Station & station = stations[stationId];
        region(station){
           int myTicket = station.nextTicket++;
           // cekamo red na stanici
           await(station.currTicket == myTicket);
           station.busId = busId;
           station.passangersChecking = station.numPassangersEntering + station.passangersExiting[busId];
           station.busPassangers = numPassangersEntering;

           // cekamo da svi putnici koji ulaze ili izlaze da provere svoj status
           await(station.passangersChecking == 0);
           station.busId = -1;
           numPassangers = station.busPassangers;

           // pustamo sledeci autobus
           station.currTicket++;
        }
        // putujemo
        stationId = (stationId +1 )%N;
    }
}

void passanger(){
    while(true){
        Station& stationFrom = stations[getStationIdFrom()];
        Station& stationTo = stations[getStationIdTo()];
        bool entrenceSuccessful = false;
        int currentBusId;

        while(!entrenceSuccessful){
            region(stationFrom) {
                // dosli smo na stanicu 
                ++stationFrom.numPassangers;
                if(stationFrom.busId == -1){
                    // cekamo autobus 
                    await(stationFrom.busId != -1);
                }

                else {
                    // autobus je vec bio tu, proveravamo status 
                    ++ stationFrom.passangersChecking;
                }

                currentBusId = stationFrom.busId;
                
                
            }
        }
    }
}

// Посматра се агенција за изнајмљивање аутомобила. У возном парку постоје 20 стандардних возила и 10 лукс возила. Приликом доласка клијента да изнајми ауто, он се изјашњава да ли жели да изнајми стандардно или лукс возило или му је све једно. Након тога он чека у реду све док му се возило не додели на коришћење. По завршетку коришћења, корисник долази још једном у агенцију и враћа ауто. У агенцији постоји један запослени који води евиденцију о томе који ауто је тренутно на коришћењу код ког корисника. Клијентима није дозвољено напуштање агенције све док запослени не обради њихов захтев за преузимање или враћање возила. Користећи регионе написати методу које се позива приликом доласка клијента да изнајми ауто, методу које се позива приликом доласка клијента да врати ауто и методу која симулира рад запосленог, као и код за иницијализацију. Потребно је обезбедити да возила не стоје на паркингу агенције, уколико постоји било који клијент који жели да изнајми тај тип возила.

#include <map>
#include <queue>

using namespace std;

// У возном парку постоје 20 стандардних возила и 10 лукс возила.
const int STD_CARS = 20;
const int LUX_CARS = 10;

// Strukture za upucivanje zahteva zaposlenom
struct Request {
    int customerId;
    unsigned place;
};

enum RequestType {
    STANDARD_VEHICLE,
    Luxury_VEHICLE,
    ANY_VEHICLE,
    RETURN_VEHICLE
};

// Monitor
struct CarDealership {
    queue<Request> standardRequests;
    queue<Request> luxuryRequests;
    queue<Request> anyRequests;
    queue<Request> returnRequests;

    map<int, int> rentedCars;
    int place;
};
CarDelership dealership;

// These queues can be changed only by the emploee, there is no need for them to be in a region.
queue<int> standardCars;
queue<int> luxuryCars;


int rentCar(int customerId, int which) {
    region (dealership) {
        unsigned myPlace = dealership.place++;
        switch (which) {
            case STANDARD_VEHICLE:
                dealership.standardRequests.push({customerId, myPlace});
                break;
            case Luxury_VEHICLE:
                dealership.luxuryRequests.push({customerId, myPlace});
                break;
            case ANY_VEHICLE:
                dealership.anyRequest.push({customerId, myPlace});
                break;
        }
        await (dealership.rentedCars[customerId]);
    }
}

void returnCar (int customerId) {
    region ( dealership ) {
        unsigned myPlace = dealership.place++;
        dealership.returnRequest.push({customerId, myPlace});
        await(!dealership.rentedCars[customerId]);
    }
}


void employee () {
    while(true){
        Request reql
        int resuest = 0;

        region(dealership) {
            await(
                dealership.standardRequests.size() +
                dealership.luxuryRequests.size() +
                dealership.anyRequest.size() +
                dealership.returnRequest.size()  > 0
            );
            unsigned minPlace = -1;
            if (!dealership.standardRequests.empty() &&
                !standardCars.empty() &&
                dealership.standardRequests.front().place < minPlace;
            ) {
                minPlace = dealership.standardRequests.front().place;
                request = STANDARD_VEHICLE;
            }

            if ( !dealership.luxuryRequests.empty() &&
                !luxuryCars.empty() &&
                dealership.luxuryRequests.front().place < minPlace
            ) {
                minPlace = dealership.luxuryRequests.front().place;
                request = LUXURY_VEHICLE;
            }
            if (!dealership.anyRequests.empty() &&
                (!standardCars.empty() || !luxuryCars.empty()) &&
                dealership.anyRequests.front().place < minPlace
            ) {
                minPlace = dealership.anyRequests.front().place;
                request = ANY_VEHICLE;
            }
            if (!dealership.returnRequests.empty() && dealership.returnRequests.front().place < minPlace) {
                minPlace = dealership.returnRequests.front().place;
                request = RETURN_VEHICLE;
            }

            switch (request) {
                case STANDARD_VEHICLE:
                    req = dealership.standardRequests.front();
                    dealership.standardRequests.pop();
                    break;
                case LUXURY_VEHICLE:
                    req = dealership.luxuryRequests.front();
                    dealership.luxuryRequests.pop();
                    break;
                case ANY_VEHICLE:
                    req = dealership.anyRequests.front();
                    dealership.anyRequests.pop();
                    break;
                case RETURN_VEHICLE:
                    req = dealership.returnRequests.front();
                    dealership.returnRequests.pop();
                    break;
            }
            }
        // Овде запослени ради неки свој посао бележења
        region (dealership) {
            switch (request) {
                case STANDARD_VEHICLE:
                    dealership.rentedCars[req.customerId] = standardCars.front();
                    standardCars.pop();
                    break;
                case LUXURY_VEHICLE:
                    dealership.rentedCars[req.customerId] = luxuryCars.front();
                    luxuryCars.pop();
                    break;
                case ANY_VEHICLE:
                    if (standardCars.empty()) {
                        dealership.rentedCars[req.customerId] = luxuryCars.front();
                        luxuryCars.pop();
                    } else {
                        dealership.rentedCars[req.customerId] = standardCars.front();
                        standardCars.pop();
                    }
                    break;
                case RETURN_VEHICLE:
                    int carId = dealership.rentedCars[req.customerId];
                    dealership.rentedCars[req.customerId] = 0;
                    if (carId > 20) {
                        luxuryCars.push(carId);
                    } else {
                        standardCars.push(carId);
                    }
                    break;
            }
        }
    }
}



int main(){
    for(int i=0; i < STD_CARS; ++i){
        standardCars.push(i+1);
    }

    for(int i=0; i < LUX_CARS; ++i){
        luxuryCars.push(i+STD_CARS+1);
    }
    return 0;
}





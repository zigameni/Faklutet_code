proizvodi = {
    "p1": {
        "ime": "Proizvod 1",
        "opis": "Opis Proizvod 1"
    },
    "p2":{
        "ime": "Proizovd 2",
        "opis": "Opis proizvod 2"
    }
}

def dohvati_sve_proizvode():
    return proizvodi.items();

def dohvati_proizvod(id): 
    return proizvodi[id];

def dodaj_proizvod(ime, opis):
    id = "p" + str(len(proizvodi)+1);
    proizvodi[id] = {"ime": ime, "opis": opis};
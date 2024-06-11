proizvodi = {
    "p1": {
        "ime": "Proizvod 1",
        "opis": "Opis proizvoda 1"
    },
    "p2": {
        "ime": "Proizvod 2",
        "opis": "Opis proizvoda 2"
    }
}

def dohvati_sve_proizvode():
    print(proizvodi.items());
    return proizvodi.items();

def dohvati_proizvod(id):
    return proizvodi[id];

def dodaj_proizvod(ime, opis):
    id = "p"+ str(len(proizvodi)+1)
    proizvodi[id] = {"ime": ime, "opis": opis};
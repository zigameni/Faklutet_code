import models;

def index(request):
    proizvodi = "";
    for k, v in models.dohvati_sve_proizvode():
        proizvodi += f"<option value=`{k}`>{v['ime']}</option>";
    return "index.html", {"proizvodi": proizvodi};

def results(request): 
    proizvod = models.dohvati_proizvod(request["body"]["proizvodi"]);
    return "results.html", {"proizvod": proizvod['ime'] + ": "+proizvod["opis"]};

def view_add_proizovd(request):
    return "add_proizvod.html", {};

def add_proizvod(request):
    models.dodaj_proizvod(request["body"]["ime"], request["body"]["opis"]);
    proizvodi = "";
    for k, v in models.dohvati_sve_proizvode():
        proizvodi += f"<option value='{k}'>{v['ime']}</option>"
    return "index.html", {"proizvodi": proizvodi};

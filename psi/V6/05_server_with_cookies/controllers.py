import models
from http import cookies;

def index(request):
    proizvodi = "";
    for key, value in models.dohvati_sve_proizvode():
        proizvodi +=f"<option value='{key}'>{value['ime']}</option>"
    return "index.html", {"proizvodi":proizvodi}, []


def results(request):
    cookie = cookies.SimpleCookie(request['cookies']);
    cookie['proizvodi'] = request["body"]["proizvodi"];
    cookie['broj']= request["body"]["broj"];
    proizvod = models.dohvati_proizvod(cookie['proizvodi'].value);
    # we need to return the page which is results.html, the data, which is proizvod and number, the number comes from cookies, and at the end we return the cookies array as well. 
    return "results.html", {"proizvod": proizvod['ime'] + proizvod["opis"], "broj": cookie['broj'].value}, [cookie['proizvodi'].output(header=''), cookie['broj'].output(header='')];


def view_cart(request):
    cookie = cookies.SimpleCookie(request['cookies']);
    try: 
        proizvod = models.dodaj_proizvod(cookie['proizvodi'].value)
        return "results.html", {"proizvod": proizvod['ime'] + ": " + proizvod["opis"], "broj": cookie['broj'].value}, [];
    except:
        return "results.html", {"proizvod": "Vasa korpa je prazna!", "broj": ""}, []
    
def view_add_proizvod(request):
    return "add_proizvod.html", {}, [];

def add_proizvod(request):
    models.dodaj_proizvod(request["body"]["ime"], request["body"]["opis"])
    proizvodi = ""
    for k, v in models.dohvati_sve_proizvode():
        proizvodi += f"<option value='{k}'>{v['ime']}</option>"
    return "index.html", {"proizvodi": proizvodi}, []


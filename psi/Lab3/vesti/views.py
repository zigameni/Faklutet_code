from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django.http import HttpRequest
from django.shortcuts import render, redirect

from vesti.forms import SearchForm, KorisnikCreationForm, VestForm
from vesti.models import Vest, Korisnik


# Create your views here.

def index(request: HttpRequest):
    searchform = SearchForm(data=request.POST or None);

    vesti = []
    if searchform.is_valid():
        term = searchform.cleaned_data.get('term');
        vesti = Vest.objects.filter(sadrzaj__contains=term);
    else:
        vesti = Vest.objects.order_by('-timestamp');

    context = {
        'searchform': SearchForm,
        'vesti': vesti,
        'vestForm': VestForm()
    }
    return render(request, 'vesti/index.html', context);


def login_req(request: HttpRequest):
    form = AuthenticationForm(data=request.POST or None);

    if form.is_valid():
        username = form.cleaned_data.get('username');
        password = form.cleaned_data.get('password');
        user = authenticate(username=username, password=password);

        if user:
            login(request, user);
            messages.info(request, 'Logged in successfully!');
            return redirect('home');
    else:
        messages.error(request, 'Login Fail!');
    context = {
        'form': form
    }

    return render(request, 'registration/login.html', context);


def logout_req(request: HttpRequest):
    logout(request);
    return redirect('home');


def registration(request: HttpRequest):
    form = KorisnikCreationForm(request.POST);
    if form.is_valid():
        user: Korisnik = form.save();
        group = Group.objects.get(name='default');
        user.groups.add(group);
        login(request, user);
        return redirect('home');

    context = {
        'form': form
    }

    return render(request, 'registration/registration.html', context)


# create vest
@login_required(login_url='login')
def create_vest(request: HttpRequest):
    form = VestForm(request.POST or None);
    if form.is_valid():
        vest = form.save(commit=False);
        vest.autor = Korisnik.objects.get(username=request.user.get_username());
        vest.save();
        return redirect('home');

# delete vest
@login_required(login_url='login')
@permission_required('vesti.delete_vest', raise_exception=True)
def delete_vest(request: HttpRequest):
    vest_id = request.POST.get('vest_id');
    if vest_id is not None:
        vest = Vest.objects.get(pk=vest_id);
        if vest.autor == request.user or request.user.has_perm('vesti.delete_vest'):
            vest.delete();

    return redirect('home');

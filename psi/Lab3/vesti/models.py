import datetime

from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class Korisnik(AbstractUser): # we need to set the costum user in settings.py
    br_obavljenih_vesti = models.IntegerField(default=0);


class Vest(models.Model):
    autor = models.ForeignKey(Korisnik, on_delete=models.CASCADE); # we set the author to be a user.
    naslov = models.CharField(max_length=50);
    sadrzaj = models.CharField(max_length=300);
    timestamp = models.DateTimeField(default=datetime.datetime.now);

    class Meta:
        db_table = 'Vest'; # name of the table in the database.

class Komentar(models.Model):
    vest = models.ForeignKey(Vest, on_delete=models.CASCADE);
    autor = models.ForeignKey(Korisnik, on_delete=models.CASCADE);
    sadrzaj = models.CharField(max_length=300);
    timestamp = models.DateTimeField(default=datetime.datetime.now);

    class Meta:
        db_table = 'Komentar';
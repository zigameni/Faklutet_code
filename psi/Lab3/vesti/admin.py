from django.contrib import admin

from vesti.models import Vest, Korisnik, Komentar

# Register your models here.
admin.site.register(Vest)
admin.site.register(Korisnik)
admin.site.register(Komentar)
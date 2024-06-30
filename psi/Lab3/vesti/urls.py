from django.urls import path

from vesti import views
from vesti.views import *

urlpatterns = [
    path('', index, name='home'),
    path('login/', login_req, name='login'),
    path('logout/', logout_req, name='logout'),
    path('register/', registration, name='register'),
    path('create_vest/', create_vest, name='create_vest'),
    path('delete_vest/', delete_vest, name='delete_vest')
]
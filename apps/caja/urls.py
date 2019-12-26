from django.urls import path

from apps.caja import views
from django.contrib.auth.decorators import login_required
app_name='caja'
urlpatterns = [    
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('home', views.home, name='home'),
    path('recibo', views.recibo, name='recibo'),
]
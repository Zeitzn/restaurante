from django.urls import path

from apps.producto import views
from django.contrib.auth.decorators import login_required
app_name='producto'
urlpatterns = [
    
    path('', views.index, name='index'),
   
]
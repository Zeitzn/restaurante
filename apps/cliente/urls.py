from django.urls import path

from apps.cliente import views
from django.contrib.auth.decorators import login_required
app_name='cliente'
urlpatterns = [    
    # path('register', views.register, name='register'),
    # path('delete', views.delete, name='delete'),
    # path('cocina', views.cocina, name='cocina'),
    # path('listaPedidos', views.listaPedidos, name='listaPedidos'),
    path('getByDoc/<doc>', views.getByDoc, name='getByDoc'),
    # #API
    # path('api/listDetalle', views.ListAllView.as_view(), name='listDetalle'),
]
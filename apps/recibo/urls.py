from django.urls import path

from apps.recibo import views
from django.contrib.auth.decorators import login_required
app_name='recibo'
urlpatterns = [    
    path('factura/<mesa>/<cliente>/<ruc>/<direccion>/<total_letras>', views.generarFactura, name='generarFactura'),   
    path('boleta/<mesa>/<cliente>/<ruc>/<direccion>', views.generarBoleta, name='generarBoleta'),   
]
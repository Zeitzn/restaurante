from django.shortcuts import render
from .models import Producto
from apps.categoria.models import Categoria
# Create your views here.

def index(request):
    oProductos=Producto.objects.all()
    oCategorias=Categoria.objects.all()
    context={
        'productos':oProductos,
        'categorias':oCategorias
    }
    return render(request,'mesero/index.html',context)
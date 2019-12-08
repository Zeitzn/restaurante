from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login
from apps.pedido.models import Pedido
# Create your views here.

def index(request):
    return render(request,'registration/login.html')

@csrf_exempt
def login(request):   
    try:        
        username=request.POST['username']
        password=request.POST['password']
        print(username)
        print(password)
        usuario=authenticate(request,username=username, password=password)
        if usuario is not None:
            auth_login(request, usuario)
            response='success'           
        else:
            response='error'           
        return HttpResponse(str(response))
    except Exception as e:
        response=e
        
        return HttpResponse(str(response))

def home(request):
    # pedidos=Pedido.objects.all().values('mesa')
    # pedidos=Pedido.objects.raw('select * from pedido group by mesa')
    pedidos=Pedido.objects.raw('select id,mesa,SUM(total) AS total from pedido where activo=1 GROUP BY mesa')
    context={
        'pedidos':pedidos
    }
    return render(request,'caja/home.html',context)
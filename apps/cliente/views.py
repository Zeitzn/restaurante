from django.shortcuts import render
from django.http import HttpResponse
from apps.cliente.models import Cliente
from django.core import serializers
# Create your views here.

def getByDoc(request, doc):
    oCliente=Cliente.objects.filter(numero=doc)

    data = serializers.serialize(
        'json', 
        oCliente
        )
    return HttpResponse(data, content_type='application/json')

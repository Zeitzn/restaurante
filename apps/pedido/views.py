from django.shortcuts import render
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from apps.producto.models import Producto
from .models import Pedido
from .models import DetallePedido
from .serializers import DetallePedidoSerializer
from django.core import serializers
from rest_framework import generics
from django.db.models import Count
from datetime import date
# Create your views here.
from django.db import connection

def cocina(request):
    return render(request,'cocina/index.html')

@csrf_exempt
def delete(request):
    if request.method=='POST':
        Datos=json.loads(request.body)
        

        DetallePedido.objects.filter(pedido_id=Datos['pedido'],producto_id=Datos['producto']).update(entregado=True)
        return HttpResponse(str('success'))

@csrf_exempt
def register(request):
    if request.method=='POST':
        Datos=json.loads(request.body)
        mesa=Datos['mesa']
        pedidos=Datos['pedidos']      

        
        
        total=0

        # for item in pedidos:
        #     for a in range(int(item['cantidad'])):
        
            
        
        for item in pedidos:
            oProducto=Producto.objects.get(id=item['producto'])
            sub_total=float(oProducto.precio)*int(item['cantidad'])
            total+=sub_total
             

        
        oPedido=Pedido(
            mesa=mesa,
            total=total
        )

        oPedido.save()
        # oProducto=Producto.objects.get(id=item['producto'])

        for item in pedidos:
            for a in range(int(item['cantidad'])):
                oProducto=Producto.objects.get(id=item['producto'])    
                oDetallePedido=DetallePedido(
                    producto=oProducto,
                    pedido=oPedido
                )
                oDetallePedido.save()

        return HttpResponse(str('success'))

def listaPedidos(request):
    # pedidos=DetallePedido.objects.values('producto').annotate(total=Count('producto'))
    # name_map = {'nombre': 'p.nombre'}
    # pedidos=DetallePedido.objects.raw('SELECT COUNT(producto_id), det.*, prod.* FROM detalle_pedido det inner join producto prod ON prod.id=det.producto_id GROUP BY det.producto_id;',translations=name_map)

    with connection.cursor() as cursor:
        # cursor.execute('SELECT COUNT(producto_id), ped.*, prod.*,ped.id AS pedido_id, prod.id AS producto_id FROM detalle_pedido det inner join producto prod ON prod.id=det.producto_id INNER JOIN pedido ped ON det.pedido_id=ped.id WHERE det.entregado=0 GROUP BY det.producto_id, ped.id ORDER BY ped.id and prod.id;')
        cursor.execute('SELECT COUNT(producto_id), prod.id AS producto_id, prod.nombre, ped.id AS pedido_id, ped.mesa FROM detalle_pedido det INNER JOIN producto prod ON prod.id=det.producto_id INNER JOIN pedido ped ON det.pedido_id=ped.id WHERE det.entregado=0 AND ped.activo=1 GROUP BY det.producto_id, ped.id ORDER BY ped.id;')
        pedidos=cursor.fetchall()
        # print(pedidos)
        diccionario_pedidos = {}
        lista_pedidos=[]

        for row in pedidos:
            print(row)
            cantidad=row[0]
            # total=row[2]
            mesa=row[4]
            nombre=row[2]
            # precio=row[7]
            pedido_id=row[3]
            producto_id=row[1]
            pedido={'cantidad':cantidad,'mesa':mesa,'nombre':nombre,'pedido':pedido_id,'producto':producto_id}
            lista_pedidos.append(pedido)

        diccionario_pedidos['pedidos']=lista_pedidos
        return HttpResponse(json.dumps(diccionario_pedidos), content_type="application/json")

def listaPedidosMesero(request):
    # pedidos=DetallePedido.objects.values('producto').annotate(total=Count('producto'))
    # name_map = {'nombre': 'p.nombre'}
    # pedidos=DetallePedido.objects.raw('SELECT COUNT(producto_id), det.*, prod.* FROM detalle_pedido det inner join producto prod ON prod.id=det.producto_id GROUP BY det.producto_id;',translations=name_map)

    with connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(producto_id), ped.*, prod.*,ped.id AS pedido_id, prod.id AS producto_id FROM detalle_pedido det inner join producto prod ON prod.id=det.producto_id INNER JOIN pedido ped ON det.pedido_id=ped.id WHERE det.entregado=0 GROUP BY det.producto_id, ped.id ORDER BY ped.id and prod.id;')
        pedidos=cursor.fetchall()
        # print(pedidos)
        diccionario_pedidos = {}
        lista_pedidos=[]

        for row in pedidos:
            print(row)
            cantidad=row[0]
            total=row[2]
            mesa=row[3]
            nombre=row[5]
            precio=row[7]
            pedido_id=row[9]
            producto_id=row[10]
            pedido={'cantidad':cantidad,'total':total,'mesa':mesa,'nombre':nombre,'precio':precio,'pedido':pedido_id,'producto':producto_id}
            lista_pedidos.append(pedido)

        diccionario_pedidos['pedidos']=lista_pedidos
        return HttpResponse(json.dumps(diccionario_pedidos), content_type="application/json")
 
def detallesMesa(request,mesa=''):
    with connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(producto_id), ped.mesa, prod.nombre, prod.precio,ped.id AS pedido_id, prod.id AS producto_id FROM detalle_pedido det inner join producto prod ON prod.id=det.producto_id INNER JOIN pedido ped ON det.pedido_id=ped.id WHERE (ped.mesa='+mesa+' AND ped.activo=1) GROUP BY det.producto_id, ped.id ORDER BY ped.id and prod.id;')
        detalles=cursor.fetchall()

        diccionario_pedidos = {}
        lista_pedidos=[]

        for row in detalles:
            cantidad=row[0]
            nombre=row[2]
            precio=row[3]
            
            pedido={'cantidad':cantidad,'nombre':nombre,'precio':precio}
            lista_pedidos.append(pedido)

        diccionario_pedidos['detalles']=lista_pedidos
        return HttpResponse(json.dumps(diccionario_pedidos), content_type="application/json")

def pagarPedido(request,mesa=''):
    with connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(producto_id), ped.mesa, prod.nombre, prod.precio,ped.id AS pedido_id, prod.id AS producto_id FROM detalle_pedido det inner join producto prod ON prod.id=det.producto_id INNER JOIN pedido ped ON det.pedido_id=ped.id WHERE (ped.mesa='+mesa+' AND ped.activo=1) GROUP BY det.producto_id, ped.id ORDER BY ped.id and prod.id;')
        detalles=cursor.fetchall()
        fecha = date.today()
        diccionario_pedidos = {}
        lista_pedidos=[]

        for row in detalles:
            oPedido=Pedido.objects.get(id=row[4])
            # oPedido.numero=numero_factura
            # oPedido.tipo='factura'
            oPedido.activo=False
            oPedido.fecha=fecha
            oPedido.save()

        diccionario_pedidos['detalles']=lista_pedidos
        return HttpResponse(json.dumps(diccionario_pedidos), content_type="application/json")

#API
class ListAllView(generics.ListAPIView):
    # permission_classes=[AllowAny]
    queryset=DetallePedido.objects.all()
    # queryset=DetallePedido.objects.all().values('producto').annotate(total=Count('producto'))
    serializer_class=DetallePedidoSerializer

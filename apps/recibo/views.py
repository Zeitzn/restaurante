from django.shortcuts import render
from apps.pedido.models import Pedido, DetallePedido
from apps.cliente.models import Cliente
from django.db.models import Count
from datetime import date
# Create your views here.
from django.db import connection
# Create your views here.
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings

from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration

def generarFactura(request, mesa='', cliente='', ruc='', direccion='', total_letras=''):

    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = "inline; filename=date-name-donation-receipt.pdf"
  
    logo = os.path.join(settings.BASE_DIR, 'static/assets/images/logo.png')
    with connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(producto_id), ped.mesa, prod.nombre, prod.precio,ped.id AS pedido_id, prod.id AS producto_id FROM detalle_pedido det inner join producto prod ON prod.id=det.producto_id INNER JOIN pedido ped ON det.pedido_id=ped.id WHERE (ped.mesa='+mesa+' AND ped.activo=1) GROUP BY det.producto_id, ped.id ORDER BY ped.id and prod.id;')
        pedidos=cursor.fetchall()

        cursor.execute('SELECT MAX(numero) FROM pedido WHERE tipo="factura"')
        result=cursor.fetchall()
        fecha = date.today()

        day=fecha.day
        month=fecha.month
        year=fecha.year

        print(len(result))
        print(result[0][0])

        if len(result)>0:
            # if result[0][0]!='':
            if result[0][0] is None:
                ultimo_numero_factura=0                
            else:
                ultimo_numero_factura=result[0][0]
        else:
            ultimo_numero_factura=0
        # print(ultimo_numero_factura[0][0])

        numero_factura=int(ultimo_numero_factura)+1
        numero_factura_vista=''

        if(numero_factura<10):
            numero_factura_vista='000000'+str(numero_factura)
        elif(numero_factura>10 and numero_factura<100):
            numero_factura_vista='00000'+str(numero_factura)
        elif(numero_factura>100 and numero_factura<1000):
            numero_factura_vista='0000'+str(numero_factura)
        elif(numero_factura>1000 and numero_factura<10000):
            numero_factura_vista='000'+str(numero_factura)
        elif(numero_factura>10000 and numero_factura<100000):
            numero_factura_vista='00'+str(numero_factura)
        elif(numero_factura>100000 and numero_factura<1000000):
            numero_factura_vista='0'+str(numero_factura)
        else:
            numero_factura_vista=str(numero_factura)
        
        diccionario_pedidos = {}
        lista_pedidos=[]
        total=0
        for row in pedidos:
            print(row)
            cantidad=int(row[0])
            nombre=row[2]
            precio=float(row[3])
            valor=cantidad*precio
            total+=valor
            pedido={'cantidad':cantidad,'nombre':nombre,'precio':precio,'valor':valor}
            lista_pedidos.append(pedido)

            oPedido=Pedido.objects.get(id=row[4])
            oPedido.numero=numero_factura
            oPedido.tipo='factura'
            oPedido.activo=False
            oPedido.fecha=fecha
            oPedido.save()

    oCliente=Cliente.objects.filter(numero=ruc)

    if len(oCliente)<1:
        oCliente=Cliente(
            nombres=cliente,
            numero=ruc,
            direccion=direccion,
            tipo='ruc'
        )
        oCliente.save()
        
    igv=total*0.18
    context={
        'logo':logo,
        'pedidos':lista_pedidos,
        'total':total,
        'igv':igv,
        'subtotal':total-igv,
        'cliente':cliente,
        'ruc':ruc,
        'direccion':direccion,
        'numero_factura':numero_factura_vista,
        'dia':day,
        'mes':getMonth(month),
        'anio':year,
        'total_letras':total_letras
    }
    html = render_to_string("recibo/factura.html",context)
    font_config = FontConfiguration()
    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, font_config=font_config)
    return response

def generarBoleta(request, mesa='', cliente='', ruc='', direccion=''):

    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = "inline; filename=date-name-donation-receipt.pdf"
  
    logo = os.path.join(settings.BASE_DIR, 'static/assets/images/logo.png')
    with connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(producto_id), ped.mesa, prod.nombre, prod.precio,ped.id AS pedido_id, prod.id AS producto_id FROM detalle_pedido det inner join producto prod ON prod.id=det.producto_id INNER JOIN pedido ped ON det.pedido_id=ped.id WHERE (ped.mesa='+mesa+' AND ped.activo=1) GROUP BY det.producto_id, ped.id ORDER BY ped.id and prod.id;')
        pedidos=cursor.fetchall()

        cursor.execute('SELECT MAX(numero) FROM pedido WHERE tipo="boleta"')
        result=cursor.fetchall()
        fecha = date.today()

        day=fecha.day
        month=fecha.month
        year=fecha.year


        if len(result)>0:            
            if result[0][0] is None:
                ultimo_numero_boleta=0                
            else:
                ultimo_numero_boleta=result[0][0]
        else:
            ultimo_numero_boleta=0
        # print(ultimo_numero_boleta[0][0])

        numero_boleta=int(ultimo_numero_boleta)+1
        numero_boleta_vista=''

        if(numero_boleta<10):
            numero_boleta_vista='000000'+str(numero_boleta)
        elif(numero_boleta>10 and numero_boleta<100):
            numero_boleta_vista='00000'+str(numero_boleta)
        elif(numero_boleta>100 and numero_boleta<1000):
            numero_boleta_vista='0000'+str(numero_boleta)
        elif(numero_boleta>1000 and numero_boleta<10000):
            numero_boleta_vista='000'+str(numero_boleta)
        elif(numero_boleta>10000 and numero_boleta<100000):
            numero_boleta_vista='00'+str(numero_boleta)
        elif(numero_boleta>100000 and numero_boleta<1000000):
            numero_boleta_vista='0'+str(numero_boleta)
        else:
            numero_boleta_vista=str(numero_boleta)
        
        diccionario_pedidos = {}
        lista_pedidos=[]
        total=0
        for row in pedidos:
            print(row)
            cantidad=int(row[0])
            nombre=row[2]
            precio=float(row[3])
            valor=cantidad*precio
            total+=valor
            pedido={'cantidad':cantidad,'nombre':nombre,'precio':precio,'valor':valor}
            lista_pedidos.append(pedido)

            oPedido=Pedido.objects.get(id=row[4])
            oPedido.numero=numero_boleta
            oPedido.tipo='boleta'
            oPedido.activo=False
            oPedido.fecha=fecha
            oPedido.save()

    oCliente=Cliente.objects.filter(numero=ruc)

    if len(oCliente)<1:
        oCliente=Cliente(
            nombres=cliente,
            numero=ruc,
            direccion=direccion,
            tipo='dni'
        )
        oCliente.save()
        
    igv=total*0.18
    context={
        'logo':logo,
        'pedidos':lista_pedidos,
        'total':total,
        'igv':igv,
        'subtotal':total-igv,
        'cliente':cliente,
        'ruc':ruc,
        'direccion':direccion,
        'numero_boleta':numero_boleta_vista,
        'dia':day,
        'mes':getMonth(month),
        'anio':year,
    }
    html = render_to_string("recibo/boleta.html",context)
    font_config = FontConfiguration()
    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, font_config=font_config)
    return response

def getMonth(data):
    if data==1:
        mes='Enero'
    elif data==2:
        mes='Febrero'
    elif data==3:
        mes='Marzo'
    elif data==4:
        mes='Abril'
    elif data==5:
        mes='Mayo'
    elif data==6:
        mes='Junio'
    elif data==7:
        mes='Julio'
    elif data==8:
        mes='Agosto'
    elif data==9:
        mes='Setiembre'
    elif data==10:
        mes='Octubre'
    elif data==11:
        mes='Noviembre'
    else:
        mes='Diciembre'
    return mes

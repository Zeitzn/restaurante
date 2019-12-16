from django.db import models
from apps.producto.models import Producto
from apps.cliente.models import Cliente
# Create your models here.
class Pedido(models.Model):
    cliente=models.ForeignKey(Cliente,on_delete=models.CASCADE, null=True)
    total=models.CharField(max_length=20)
    mesa=models.CharField(max_length=3)
    activo=models.BooleanField(default=True)
    tipo=models.CharField(max_length=7, null=True)
    numero=models.CharField(max_length=7, null=True)
    fecha=models.DateField(null=True)
    class Meta:
        db_table='pedido'
    def __str__(self):
        return '%s' % (self.total)

class DetallePedido(models.Model):
    pedido=models.ForeignKey(Pedido,on_delete=models.CASCADE, null=True)
    producto=models.ForeignKey(Producto,on_delete=models.CASCADE, null=True)
    entregado=models.BooleanField(default=False)
    class Meta:
        db_table='detalle_pedido'
    def __str__(self):
        return '%s' % (self.producto)
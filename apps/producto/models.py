from django.db import models
from apps.categoria.models import Categoria
# Create your models here.

class Producto(models.Model):
    categoria=models.ForeignKey(Categoria,on_delete=models.CASCADE, null=True)
    nombre=models.CharField(max_length=100)
    descripcion=models.CharField(max_length=200)
    precio=models.CharField(max_length=20)

    class Meta:
        db_table='producto'
    def __str__(self):
        return '%s' % (self.nombre)

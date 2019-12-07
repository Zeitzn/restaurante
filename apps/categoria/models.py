from django.db import models

# Create your models here.

class Categoria(models.Model):
    nombre=models.CharField(max_length=50)

    class Meta:
        db_table='categoria'

    def __str__(self):
        return '%s' % (self.nombre)
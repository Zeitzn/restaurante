from django.db import models

# Create your models here.

class Cliente(models.Model):
    nombres=models.CharField(max_length=200, null=True)
    direccion=models.CharField(max_length=200, null=True)
    numero=models.CharField(max_length=20, null=True)
    tipo=models.CharField(max_length=3, null=True)
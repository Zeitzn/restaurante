# from rest_framework import generics
from rest_framework import serializers
from .models import Producto
# from apps.tipo.serializers import TipoSerializer

class ProductoSerializer(serializers.ModelSerializer):
    # tipo = TipoSerializer(many=False)
    class Meta:
        model = Producto
        fields = '__all__'
        depth = 1
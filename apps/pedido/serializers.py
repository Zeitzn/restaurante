# from rest_framework import generics
from rest_framework import serializers
from .models import DetallePedido
# from apps.tipo.serializers import TipoSerializer

class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = '__all__'
        depth = 2


# class DetallePedidoSerializer(serializers.ModelSerializer):
#     total=serializers.IntegerField()
#     class Meta:
#         model = DetallePedido
#         fields = ('id','producto','total')
#         # depth = 2
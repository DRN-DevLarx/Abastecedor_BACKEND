from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Categoria, Proveedor, Producto, InformacionUsuario, 
    Pedido, DetallePedido, Venta, DetalleVenta
)

# -------------------------------
# User Serializer
# -------------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

# -------------------------------
# InformacionUsuario Serializer
# -------------------------------
class InformacionUsuarioSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = InformacionUsuario
        fields = ['id', 'user', 'identificacion', 'telefono', 'direccion']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        info_usuario = InformacionUsuario.objects.create(user=user, **validated_data)
        return info_usuario

# -------------------------------
# Categoría y Proveedor
# -------------------------------
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

# -------------------------------
# Producto
# -------------------------------
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

# -------------------------------
# Pedido y DetallePedido
# -------------------------------
class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    detallepedido_set = DetallePedidoSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = '__all__'

# -------------------------------
# Venta y DetalleVenta
# -------------------------------
class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    detalleventa_set = DetalleVentaSerializer(many=True, read_only=True)

    class Meta:
        model = Venta
        fields = '__all__'

from rest_framework import serializers
from django.contrib.auth.models import User, Group
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
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        try:
            password = validated_data.pop('password', None)
            
            for attr, value in validated_data.items() :
                setattr(instance, attr, value)
                
            if password :
                instance.set_password(password)
            instance.save()
            return instance
        
        except Exception as e:
            print(f"Error al actualizar usuario: {e}") 
            raise serializers.ValidationError({"error": "No se pudo actualizar el usuario."})

# -------------------------------
# Assign Group Serializer
# -------------------------------
class AsignarGrupoSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    group_id = serializers.IntegerField()

    def validate(self, data):
        try:
            data['user'] = User.objects.get(id=data['user_id'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Usuario no existe")

        try:
            data['group'] = Group.objects.get(id=data['group_id'])
        except Group.DoesNotExist:
            raise serializers.ValidationError("Grupo no existe")

        return data

    def save(self):
        user = self.validated_data['user']
        group = self.validated_data['group']
        user.groups.add(group)  # agrega sin eliminar otros grupos
        return user

# -------------------------------
# InformacionUsuario Serializer
# -------------------------------
class InformacionUsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = InformacionUsuario
        fields = ['id', 'user', 'telefono', 'direccion']

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

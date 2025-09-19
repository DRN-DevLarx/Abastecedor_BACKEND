from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User, Group
from .models import (
    Categoria, Proveedor, Consultas, Producto, InformacionUsuario, 
    Pedido, DetallePedido, Venta, DetalleVenta, RegistroTemporal
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
# Groups Serializer
# -------------------------------
class GruposSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

# -------------------------------
# InformacionUsuario Serializer
# -------------------------------
class InformacionUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformacionUsuario
        fields = '__all__'

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
# Consultas
# -------------------------------
class ConsultasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultas
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


# -------------------------------
# Datos de Registro temporal
# -------------------------------
class RegistroTemporalSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegistroTemporal
        fields = '__all__'

# -------------------------------
# Access_token (Inicio de sesion)
# -------------------------------

class CustomTokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "error_code": "invalid_credentials",
                "message": "Credenciales incorrectas."
            })

        if not user.check_password(password):
            raise serializers.ValidationError({
                "error_code": "invalid_credentials",
                "message": "Credenciales incorrectas."
            })

        # Crear el token
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        # Agregar campos personalizados al access token
        groups = user.groups.values_list('name', flat=True)

        access_token['role'] = groups[0] if groups else None
        access_token['user_id'] = user.id
        access_token['is_active'] = user.is_active
        
        return {
            'access': str(access_token),
            'refresh': str(refresh),
            'user_id': user.id,
            'role': groups[0] if groups else None,
            'is_active': user.is_active
        }

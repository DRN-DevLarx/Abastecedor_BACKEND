from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.contrib.auth.models import User, Group
from .models import (
    Categoria, Proveedor, Consultas, Producto, ImagenesProducto, InformacionUsuario, ImagenesUsuario, Carrito, DetalleCarrito,
    Pedido, DetallePedido, RegistroTemporal,
    ImagenesCarrusel, ContenidoEstatico, Comentarios
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
# Serializer de asignar relacion grupo usuario
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
# Serializer de eliminar relacion grupo usuario
# -------------------------------
class EliminarUsuarioSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate(self, data):
        try:
            data['user'] = User.objects.get(id=data['ID'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Usuario no existe")
        return data

    def save(self):
        user = self.validated_data['user']
        
        # 1. Eliminar relaciones con grupos
        user.groups.clear()
        
        # 2. Eliminar usuario (con CASCADE se borran sus datos en InformacionUsuario)
        username = user.username  # guardamos el nombre para mostrar en la respuesta
        user.delete()
        
        return username

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
# Imagenes de usuario
# -------------------------------
class ImagenesUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenesUsuario
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
# Imagenes Carrusel
# -------------------------------
class ImagenesCarruselSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenesCarrusel
        fields = '__all__'

# -------------------------------
# Contenido Estatico
# -------------------------------
class ContenidoEstaticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContenidoEstatico
        fields = '__all__'

# -------------------------------
# Comentarios
# -------------------------------
class ComentariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentarios
        fields = '__all__'

# -------------------------------
# Producto
# -------------------------------
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

# -------------------------------
# Imagenes de Produco
# -------------------------------
class ImagenesProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenesProducto
        fields = '__all__'

class ProductoMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = (
            "id",
            "codigo",
            "nombre",
            "precio",
            "stock",
            "referenciaIMG",
        )

class DetalleCarritoSerializer(serializers.ModelSerializer):
    
    # 🔹 para lectura
    producto = ProductoMiniSerializer(read_only=True)

    producto_id = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(),
        source="producto",
        write_only=True
    )

    class Meta:
        model = DetalleCarrito
        fields = [
            "id",
            "producto",          # 👈 objeto completo (read)
            "producto_id",
            "cantidad",
            "precio_unitario",
            "subtotal",
            "seleccionado",
        ]
        read_only_fields = ["precio_unitario", "subtotal"]

    def create(self, validated_data):
        producto = validated_data["producto"]
        cantidad = validated_data["cantidad"]
        carrito = self.context["carrito"]

        detalle, creado = DetalleCarrito.objects.get_or_create(
            carrito=carrito,
            producto=producto,
            defaults={
                "cantidad": cantidad,
                "precio_unitario": producto.precio,
            }
        )

        if not creado:
            detalle.cantidad += cantidad

        detalle.precio_unitario = producto.precio
        detalle.save()
        carrito.recalcular_totales()
        return detalle

class CarritoSerializer(serializers.ModelSerializer):
    items = DetalleCarritoSerializer(many=True, read_only=True)
    usuario = serializers.ReadOnlyField(source="usuario.username")

    class Meta:
        model = Carrito
        fields = "__all__"
        read_only_fields = ["subtotal", "total", "fecha_creacion", "fecha_actualizacion"]


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

        access_token['user_id'] = user.id
        access_token['username'] = user.username
        access_token['role'] = groups[0] if groups else None
        access_token['is_superuser'] = user.is_superuser
        access_token['is_active'] = user.is_active
        
        return {
            'access': str(access_token),
            'refresh': str(refresh)
        }

class CustomTokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh_token = attrs.get("refresh")

        try:
            # Validar el refresh token
            refresh = RefreshToken(refresh_token)
            user_id = refresh["user_id"]
            user = User.objects.get(id=user_id)

            # Crear un nuevo access token
            access_token = refresh.access_token

            # Agregar campos personalizados
            groups = user.groups.values_list('name', flat=True)
            access_token["user_id"] = user.id
            access_token["username"] = user.username
            access_token["role"] = groups[0] if groups else None
            access_token["is_superuser"] = user.is_superuser
            access_token["is_active"] = user.is_active

            return {
                "access": str(access_token)
            }

        except TokenError:
            raise serializers.ValidationError({"error": "Refresh token inválido o expirado"})
        except User.DoesNotExist:
            raise serializers.ValidationError({"error": "Usuario no encontrado"})

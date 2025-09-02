# Envio de codigo al correoimport random
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils.crypto import get_random_string
from django.utils import timezone
import random

from django.contrib.auth.models import User
from .models import (
    Categoria, Proveedor, Producto, InformacionUsuario, 
    Pedido, DetallePedido, Venta, DetalleVenta, CodigoVerificacion
)
from .serializers import (
    UserSerializer, CategoriaSerializer, ProveedorSerializer, ProductoSerializer,
    InformacionUsuarioSerializer, PedidoSerializer, DetallePedidoSerializer,
    VentaSerializer, DetalleVentaSerializer
)
# -------------------------------
# User
# -------------------------------
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# -------------------------------
# InformacionUsuario
# -------------------------------
class InformacionUsuarioListCreateView(generics.ListCreateAPIView):
    queryset = InformacionUsuario.objects.all()
    serializer_class = InformacionUsuarioSerializer

class InformacionUsuarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InformacionUsuario.objects.all()
    serializer_class = InformacionUsuarioSerializer

# -------------------------------
# Categoria
# -------------------------------
class CategoriaListCreateView(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class CategoriaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

# -------------------------------
# Proveedor
# -------------------------------
class ProveedorListCreateView(generics.ListCreateAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class ProveedorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

# -------------------------------
# Producto
# -------------------------------
class ProductoListCreateView(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ProductoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

# -------------------------------
# Pedido
# -------------------------------
class PedidoListCreateView(generics.ListCreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class PedidoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

# -------------------------------
# DetallePedido
# -------------------------------
class DetallePedidoListCreateView(generics.ListCreateAPIView):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer

class DetallePedidoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer

# -------------------------------
# Venta
# -------------------------------
class VentaListCreateView(generics.ListCreateAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

class VentaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

# -------------------------------
# DetalleVenta
# -------------------------------
class DetalleVentaListCreateView(generics.ListCreateAPIView):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer

class DetalleVentaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer

# -------------------------------
# Código de verificacion
# -------------------------------

class EnviarCodigoGenericoView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        
        email = request.data.get("correo")
        nombre = request.data.get("nombre")

        if not email:
            return Response({'error': 'Correo es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)

        # Generar código de 6 dígitos
        codigo = get_random_string(length=6, allowed_chars='0123456789')

        # Guardar código en la base de datos con expiración de 5 minutos
        CodigoVerificacion.objects.create(
            correo=email,
            codigo=codigo,
            expiracion=timezone.now() + timedelta(minutes=5)
        )
        
        # Enviar el correo
        asunto = "Tu código de verificación"
        cuerpo = f"""
        Hola {nombre},

        Tu código de verificación es: {codigo}
        Este código caduca en 5 minutos y solo puede ser usado una vez.

        Saludos,
        Equipo de soporte
        """.strip()

        send_mail(
            subject=asunto,
            message=cuerpo,
            from_email=None,  # Usará DEFAULT_FROM_EMAIL
            recipient_list=[email],
            fail_silently=False
        )

        return Response({'mensaje': 'Correo enviado con el código'}, status=status.HTTP_200_OK)


# -------------------------------
# Validar codigo
# -------------------------------

class ValidarCodigoView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        correo = request.data.get("correo")
        codigo = request.data.get("codigo")

        print("correo", correo)
        print("codigo", codigo)
        
        if not correo or not codigo:
            return Response({"error": "Correo y código son obligatorios"}, status=400)

        try:
            codigo_obj = CodigoVerificacion.objects.filter(
                correo=correo, codigo=codigo, usado=False
            ).latest("creado_en")

        except CodigoVerificacion.DoesNotExist:
            return Response({"error": "Código inválido"}, status=404)

        # Verificar expiración
        if timezone.now() > codigo_obj.expiracion:
            return Response({"error": "El código ha expirado"}, status=400)

        # Marcar como usado
        codigo_obj.usado = True
        codigo_obj.save()

        return Response({"mensaje": "Código válido"}, status=200)


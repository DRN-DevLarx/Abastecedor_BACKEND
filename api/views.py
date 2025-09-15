# Envio de codigo al correoimport random
from datetime import datetime, timedelta
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils.crypto import get_random_string
from django.utils import timezone
import smtplib
from django.utils.http import http_date

from django.contrib.auth.models import User
from .models import (
    Categoria, Proveedor, Producto, InformacionUsuario, 
    Pedido, DetallePedido, Venta, DetalleVenta, CodigoVerificacion, RegistroTemporal
)
from .serializers import (
    UserSerializer, InformacionUsuarioSerializer, AsignarGrupoSerializer, CategoriaSerializer, 
    ProveedorSerializer, ProductoSerializer, PedidoSerializer, DetallePedidoSerializer, VentaSerializer, 
    DetalleVentaSerializer, RegistroTemporalSerializer
)
# -------------------------------
# User
# -------------------------------
class UserListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# -------------------------------
# InformacionUsuario
# -------------------------------
class InformacionUsuarioListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    queryset = InformacionUsuario.objects.all()
    serializer_class = InformacionUsuarioSerializer

class InformacionUsuarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InformacionUsuario.objects.all()
    serializer_class = InformacionUsuarioSerializer

# -------------------------------
# AsignarGrupo
# -------------------------------
class AsignarGrupoView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = AsignarGrupoSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message": f"Grupo asignado a {user.username}"}, status=status.HTTP_200_OK)

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
# Registro temporal
# -------------------------------
class RegistroTemporalListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = RegistroTemporal.objects.all()
    serializer_class = RegistroTemporalSerializer

class RegistroTemporalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RegistroTemporal.objects.all()
    serializer_class = RegistroTemporalSerializer

# -------------------------------
# Código de verificacion
# -------------------------------
class EnviarCodigoGenericoView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Obtener datos del frontend
        nombre = request.data.get("nombre")
        apellido = request.data.get("apellido")
        username = request.data.get("username")
        phone = request.data.get("telefono")
        email = request.data.get("correo")

        # Validar campos obligatorios
        if not email or not nombre or not username:
            return Response(
                {'error': 'Nombre, correo y username son obligatorios.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Guardar o actualizar registro temporal
        registro_temp, _ = RegistroTemporal.objects.update_or_create(
            email=email,
            defaults={
                "nombre": nombre,
                "apellido": apellido,
                "username": username,
                "phone": phone
            }
        )

        # Obtener o crear registro de código
        registro, creado = CodigoVerificacion.objects.get_or_create(
            correo=email,
            defaults={
                "codigo": "",
                "expiracion": timezone.now(),
                "intentos": 0,
                "proximo_reenvio": timezone.now()
            }
        )

        # Verificar cooldown
        if timezone.now() < registro.proximo_reenvio:
            segundos_restantes = int((registro.proximo_reenvio - timezone.now()).total_seconds())
            return Response(
                {"error": f"Debes esperar {segundos_restantes} segundos antes de reenviar.",
                 "wait_time": segundos_restantes},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        # Generar nuevo código
        codigo = get_random_string(length=6, allowed_chars="0123456789")
        registro.codigo = codigo
        registro.expiracion = timezone.now() + timedelta(minutes=5)
        registro.usado = False
        registro.intentos += 1

        # Cooldown progresivo (30s, 60s, 90s..., máximo 300s)
        wait_time = min(registro.intentos * 30, 300)
        registro.proximo_reenvio = timezone.now() + timedelta(seconds=wait_time)
        registro.save()

        # Enviar correo
        asunto = "Tu código de verificación"
        cuerpo = f"""
        Hola {nombre},

        Tu código de verificación es: {codigo}
        Este código caduca en 5 minutos y solo puede usarse una vez.

        Saludos,
        Equipo de soporte
        """.strip()

        try:
            send_mail(
                subject=asunto,
                message=cuerpo,
                from_email=None,  # usa DEFAULT_FROM_EMAIL
                recipient_list=[email],
                fail_silently=False
            )
        except Exception:
            return Response({'error': 'No se pudo enviar el correo'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Respuesta final
        response = Response()

        response.data = {
            "mensaje": f"Correo enviado.",
            "wait_time": wait_time
        }

        return response


# -------------------------------
# Reenviar codigo
# -------------------------------

class ReenviarCodigoView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("correo")
        nombre = request.data.get("nombre")

        if not email or not nombre:
            return Response(
                {"error": "Correo y nombre son obligatorios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Buscar el registro de verificación o crearlo si no existe
        registro, _ = CodigoVerificacion.objects.get_or_create(
            correo=email,
            defaults={
                "codigo": "",
                "expiracion": timezone.now(),
                "intentos": 0,
                "proximo_reenvio": timezone.now()
            }
        )

        # Verificar si ya debe esperar antes de reenviar
        if timezone.now() < registro.proximo_reenvio:
            segundos_restantes = int((registro.proximo_reenvio - timezone.now()).total_seconds())

            return Response(
                {
                    "error": f"Debes esperar {segundos_restantes} segundos antes de reenviar.",
                    "wait_time": segundos_restantes
                },
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        # Generar nuevo código
        codigo = get_random_string(length=6, allowed_chars="0123456789")
        registro.codigo = codigo
        registro.expiracion = timezone.now() + timedelta(minutes=5)
        registro.usado = False
        registro.intentos += 1

        # Tiempo de espera incremental (30s, 60s, ..., máx 300s)
        wait_time = min(registro.intentos * 30, 300)
        registro.proximo_reenvio = timezone.now() + timedelta(seconds=wait_time)
        registro.save()

        # Enviar el correo con el nuevo código
        asunto = "Tu nuevo código de verificación"
        cuerpo = f"""
        Hola {nombre},

        Tu nuevo código de verificación es: {codigo}
        Este código caduca en 5 minutos y solo puede usarse una vez.

        Saludos,
        Equipo de soporte
        """.strip()

        try:
            send_mail(
                subject=asunto,
                message=cuerpo,
                from_email=None,  # Usa DEFAULT_FROM_EMAIL
                recipient_list=[email],
                fail_silently=False
            )
        except Exception as e:
            return Response(
                {"error": f"No se pudo enviar el correo: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {
                "mensaje": "Código reenviado correctamente.",
                "wait_time": wait_time
            },
            status=status.HTTP_200_OK
        )


# -------------------------------
# Validar codigo
# -------------------------------

class ValidarCodigoView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        correo = request.data.get("correo")
        codigo = request.data.get("codigo")

        if not correo or not codigo:
            return Response(
                {"error": "Correo y código son obligatorios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Buscar el último registro con ese correo, código y no usado
        try:
            registro = CodigoVerificacion.objects.filter(
                correo=correo,
                codigo=codigo,
                usado=False
            ).latest("creado_en")
        except CodigoVerificacion.DoesNotExist:
            return Response(
                {"error": "Código incorrecto o ya fue utilizado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar expiración
        if timezone.now() > registro.expiracion:
            return Response(
                {"error": "El código ha expirado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Marcar como usado
        registro.usado = True
        registro.save()

        return Response(
            {
                "mensaje": "Código validado correctamente.",
                "correo": registro.correo  # confirmamos el correo desde el modelo
            },
            status=status.HTTP_200_OK
        )


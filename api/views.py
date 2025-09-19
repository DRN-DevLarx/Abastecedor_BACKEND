# Envio de codigo al correoimport random
from datetime import datetime, timedelta
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils.crypto import get_random_string
from django.utils import timezone
from rest_framework_simplejwt.views import TokenObtainPairView

from .permission import IsAuthenticatedAllowInactive
from .authentication import JWTAllowInactiveAuthentication

from django.contrib.auth.models import User, Group
from .models import (
    Categoria, Proveedor, Consultas, Producto, InformacionUsuario, 
    Pedido, DetallePedido, Venta, DetalleVenta, CodigoVerificacion, RegistroTemporal
)
from .serializers import (
    UserSerializer, InformacionUsuarioSerializer, AsignarGrupoSerializer, GruposSerializer, CategoriaSerializer, 
    ProveedorSerializer, ConsultasSerializer, ProductoSerializer, PedidoSerializer, DetallePedidoSerializer, VentaSerializer, 
    DetalleVentaSerializer, RegistroTemporalSerializer, CustomTokenObtainPairSerializer
)
# -------------------------------
# User
# -------------------------------
class UserListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    
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
# Grupos
# -------------------------------
class GruposListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    queryset = Group.objects.all()
    serializer_class = GruposSerializer

# class GruposDetailView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [AllowAny]
    
#     queryset = Group.objects.all()
#     serializer_class = GruposSerializer

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
# Consultas
# -------------------------------
class ConsultasListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny] 
    
    queryset = Consultas.objects.all()
    serializer_class = ConsultasSerializer

class ConsultasDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]

    queryset = Consultas.objects.all()
    serializer_class = ConsultasSerializer

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
class ValidarCodigoView(generics.GenericAPIView):
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

# -------------------------------
# Vista del access_token
# -------------------------------
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDataView(APIView):
    authentication_classes = [JWTAllowInactiveAuthentication]
    permission_classes = [IsAuthenticatedAllowInactive]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

# -------------------------------
# Enviar contraseña temporal
# -------------------------------
class EnviarClaveTemporalView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("correo")

        if not email:
            return Response({'error': 'El correo electrónico es obligatorio.'}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'No existe un usuario con ese correo electrónico.'}, status=404)

        # Generar clave temporal (8 caracteres alfanuméricos)
        clave_temporal = get_random_string(length=8)

        # Guardar nueva clave y desactivar usuario
        user.set_password(clave_temporal)
        user.is_active = False
        user.save()

        # Enviar el correo
        asunto = "Tu contraseña temporal"
        cuerpo = f"""
        Hola {user.first_name},

        Se ha solicitado el restablecimiento de tu contraseña.

        Tu username es: {user.username}
        Tu nueva contraseña temporal es: {clave_temporal}

        Por seguridad, tu cuenta ha sido desactivada temporalmente. 
        Actívala iniciando sesión con esta contraseña y actualizando tu contraseña.

        Saludos,
        El equipo de soporte
        """.strip()

        send_mail(
            subject=asunto,
            message=cuerpo,
            from_email=None,
            recipient_list=[email],
            fail_silently=False
        )

        return Response({'mensaje': 'Correo enviado con la contraseña temporal.'}, status=200)

# -------------------------------
# Enviar codigo para cambio de correo
# -------------------------------
class EnviarCodigoCambioCorreoView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Obtener datos del frontend
        name = request.data.get("name")
        email = request.data.get("correo")

        # Validar campos obligatorios
        if not email or not name:
            return Response(
                {'error': 'Correo y el nombre son obligatorios.'},
                status=status.HTTP_400_BAD_REQUEST
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
        asunto = "Cambio de correo electrónico"
        cuerpo = f"""
        Hola {name},

        Estás cambiando tu correo electrónico.
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
        return Response({
            "mensaje": f"Correo enviado para cambiar la cuenta de {name}.",
            "wait_time": wait_time
        })

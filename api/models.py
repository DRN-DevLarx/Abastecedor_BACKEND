from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import uuid


# -------------------------------
# Categoría de productos
# -------------------------------
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# -------------------------------
# Proveedor
# -------------------------------
class Proveedor(models.Model):
    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

# -------------------------------
# Consultas
# -------------------------------
class Consultas(models.Model):
    user = models.CharField(max_length=10, blank=True, null=True)
    nombre_completo = models.CharField(max_length=50)
    correo = models.CharField(max_length=100)
    asunto = models.CharField(max_length=50,)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_completo} - {self.mensaje}"

# -------------------------------
# Producto
# -------------------------------
class Producto(models.Model):
    codigo = models.CharField(blank=True, null=True, max_length=15)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    calificacion = models.PositiveIntegerField(default=0)
    descripcion = models.TextField(blank=True, null=True)
    referenciaIMG = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre



# -------------------------------
# Información adicional de Usuario
# -------------------------------
class InformacionUsuario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    referenciaIMG = models.TextField(blank=True, null=True)
    notificaciones = models.BooleanField(default=False)
    tema = models.CharField(default="normal", max_length=10)

    def __str__(self):
        return f"{self.user} - {self.telefono}"


# -------------------------------
# Imagenes de Usuario
# -------------------------------
class ImagenesUsuario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.TextField(blank=True, null=True)
    fechaSubida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

# -------------------------------
# Pedido
# -------------------------------
class Pedido(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("en_proceso", "En proceso"),
        ("entregado", "Entregado"),
        ("cancelado", "Cancelado"),
    ]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")

    def total(self):
        return sum(detalle.subtotal() for detalle in self.detallepedido_set.all())

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.user.username}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

# -------------------------------
# Venta
# -------------------------------
class Venta(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.SET_NULL, null=True, blank=True)  # opcional
    cliente = models.ForeignKey(InformacionUsuario, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    empleado = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="ventas_registradas")

    def total(self):
        return sum(detalle.subtotal() for detalle in self.detalleventa_set.all())

    def __str__(self):
        return f"Venta {self.id} - {self.fecha}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

# -------------------------------
# Codigo de Verificacion
# -------------------------------
class CodigoVerificacion(models.Model):
    correo = models.EmailField()
    codigo = models.CharField(max_length=6)
    creado_en = models.DateTimeField(auto_now_add=True)   
    expiracion = models.DateTimeField()                   
    usado = models.BooleanField(default=False)            
    intentos = models.IntegerField(default=0)             
    proximo_reenvio = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return f"{self.correo} - {self.codigo} ({'usado' if self.usado else 'activo'})"


class RegistroTemporal(models.Model):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.username}"

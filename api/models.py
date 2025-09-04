from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

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
    direccion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

# -------------------------------
# Producto
# -------------------------------
class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre

# -------------------------------
# Información adicional de Usuario
# -------------------------------
class InformacionUsuario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación 1 a 1
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.telefono}"

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

    cliente = models.ForeignKey(InformacionUsuario, on_delete=models.CASCADE)
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

class CodigoVerificacion(models.Model):
    correo = models.EmailField()
    codigo = models.CharField(max_length=6)
    creado_en = models.DateTimeField(auto_now_add=True)
    expiracion = models.DateTimeField()
    usado = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Si no se establece expiración, se fija 5 minutos desde creado
        if not self.expiracion:
            self.expiracion = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)

    def esta_valido(self):
        """Devuelve True si el código no ha expirado y no ha sido usado."""
        return not self.usado and timezone.now() < self.expiracion

    def __str__(self):
        return f"{self.correo} - {self.codigo}"

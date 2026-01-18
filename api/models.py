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
    telefono2 = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

# -------------------------------
# Imagenes del carrusel Inicial
# -------------------------------
class ImagenesCarrusel(models.Model):
    subida_por = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=15, default="activa")
    url = models.TextField()
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.modificado_Por} - {self.estado}"

# -------------------------------
# Contenido estatico de la pagina
# -------------------------------
class ContenidoEstatico(models.Model):
    titulo = models.CharField(max_length=50)
    contenido = models.TextField()
    modificado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    actualizado_el = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titulo} - {self.modificado_Por} - {self.actualizado_el}"

# -------------------------------
# Contenido estatico de la pagina
# -------------------------------
class Comentarios(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField()
    publicado_el = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.comentario} - {self.publicado_el}"

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
# Comentarios sobre nosotros
# -------------------------------
# class Comentarios(models.Model):
#     user = models.CharField(max_length=10, blank=True, null=True)
#     mensaje = models.CharField(max_length=100)
#     fecha = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user} - {self.mensaje}"


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
# Imagenes de producto
# -------------------------------
class ImagenesProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    imagen = models.TextField(blank=True, null=True)
    fechaSubida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.producto

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


class Carrito(models.Model):

    ESTADOS = (
        ("ACTIVO", "Activo"),
        ("PAGO", "En proceso de pago"),
        ("COMPLETADO", "Completado"),
        ("CANCELADO", "Cancelado"),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carritos")
    estado = models.CharField(max_length=15, choices=ESTADOS, default="ACTIVO")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def recalcular_totales(self):
        subtotal = sum(item.subtotal for item in self.items.all())
        self.subtotal = subtotal
        self.total = subtotal
        self.save(update_fields=["subtotal", "total"])

    def __str__(self):
        return f"Carrito #{self.id} - {self.usuario.username} - {self.estado}"


class DetalleCarrito(models.Model):
    carrito = models.ForeignKey(Carrito,on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    seleccionado = models.BooleanField(default=True)

    class Meta:
        unique_together = ("carrito", "producto")

    def save(self, *args, **kwargs):
        self.subtotal = self.precio_unitario * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.seleccionado}] {self.producto.nombre}"


# -------------------------------
# Pedido
# -------------------------------
# 
class Pedido(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("en_preparacion", "En preparación"),
        ("empacado", "Empacado"),
        ("enviado", "Enviado"),
        ("entregado", "Entregado"),
        ("cancelado", "Cancelado"),
    ]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")
    pagado = models.BooleanField(default=False)

    fecha_pago = models.DateTimeField(null=True, blank=True)
    metodo_pago = models.CharField(max_length=50, null=True, blank=True)

    def total(self):
        return sum(d.subtotal() for d in self.detallepedido_set.all())

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.username}"

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

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


# -------------------------------
# Categoría de productos
# -------------------------------
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.nombre

# -------------------------------
# Proveedor
# -------------------------------
class Proveedor(models.Model):
    nombre = models.CharField(max_length=200, db_index=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    telefono2 = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.nombre

# -------------------------------
# Imagenes del carrusel Inicial
# -------------------------------
class ImagenesCarrusel(models.Model):
    subida_por = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    estado = models.CharField(max_length=15, default="activa", db_index=True)
    url = models.CharField(max_length=500)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.modificado_Por} - {self.estado}"

# -------------------------------
# Contenido estatico de la pagina
# -------------------------------
class ContenidoEstatico(models.Model):
    titulo = models.CharField(max_length=50, db_index=True)
    contenido = models.CharField(max_length=500, db_index=True)
    modificado_por = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    actualizado_el = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titulo} - {self.modificado_Por} - {self.actualizado_el}"

# -------------------------------
# Contenido estatico de la pagina
# -------------------------------
class Comentarios(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    comentario = models.CharField(max_length=500, )
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
    mensaje = models.CharField(max_length=500, )
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_completo} - {self.mensaje}"

# -------------------------------
# Comentarios sobre nosotros
# -------------------------------
# class Comentarios(models.Model):
#     user = models.CharField(max_length=10, blank=True, null=True)
#     mensaje = models.CharField(max_length=100)
#     fecha = models.CharField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user} - {self.mensaje}"


# -------------------------------
# Producto
# -------------------------------
class Producto(models.Model):
    codigo = models.CharField(blank=True, null=True, max_length=15, db_index=True)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    calificacion = models.PositiveIntegerField(default=0)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    referenciaIMG = models.CharField(max_length=500, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre

# -------------------------------
# Imagenes de producto
# -------------------------------
class ImagenesProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_index=True)
    imagen = models.CharField(max_length=500, blank=True, null=True)
    fechaSubida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.producto

# -------------------------------
# Información adicional de Usuario
# -------------------------------
class InformacionUsuario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=500, blank=True, null=True)
    referenciaIMG = models.CharField(max_length=500, blank=True, null=True)
    notificaciones = models.BooleanField(default=False)
    tema = models.CharField(default="normal", max_length=10)

    def __str__(self):
        return f"{self.user} - {self.telefono}"

# -------------------------------
# Imagenes de Usuario
# -------------------------------
class ImagenesUsuario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    imagen = models.CharField(max_length=500, blank=True, null=True)
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

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carritos", db_index=True)
    estado = models.CharField(max_length=15, choices=ESTADOS, default="ACTIVO", db_index=True)
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
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_index=True)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    seleccionado = models.BooleanField(default=True)

    class Meta:
        unique_together = ("carrito", "producto")

    def save(self, *args, **kwargs):
        self.subtotal = self.precio_unitario * self.cantidad
        super().save(*args, **kwargs)

        return self.producto.nombre
        

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

    cliente = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    fecha = models.DateTimeField(auto_now_add=True, db_index=True)

    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente", db_index=True)
    pagado = models.BooleanField(default=False)

    fecha_pago = models.CharField(max_length=500, null=True, blank=True)
    metodo_pago = models.CharField(max_length=50, null=True, blank=True)

    def total(self):
        return sum(d.subtotal() for d in self.detallepedido_set.all())

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.username}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, db_index=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_index=True)
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
    correo = models.EmailField(db_index=True)
    codigo = models.CharField(max_length=6, db_index=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    expiracion = models.CharField(max_length=500, db_index=True)      
    usado = models.BooleanField(default=False, db_index=True)
    intentos = models.IntegerField(default=0)
    proximo_reenvio = models.CharField(max_length=500, default=timezone.now)

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

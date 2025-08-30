from rest_framework import generics
from django.contrib.auth.models import User
from .models import (
    Categoria, Proveedor, Producto, InformacionUsuario, 
    Pedido, DetallePedido, Venta, DetalleVenta
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

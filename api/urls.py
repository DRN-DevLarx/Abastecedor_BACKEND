from django.urls import path
from . import views

urlpatterns = [
    # User
    path('api/users/', views.UserListCreateView.as_view(), name='user-list-create'),
    path('api/users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),

    # InformacionUsuario
    path('api/informacionUsuarios/', views.InformacionUsuarioListCreateView.as_view(), name='informacionusuario-list-create'),
    path('api/informacionUsuarios/<int:pk>/', views.InformacionUsuarioDetailView.as_view(), name='informacionusuario-detail'),

    # Categoria
    path('api/categorias/', views.CategoriaListCreateView.as_view(), name='categoria-list-create'),
    path('api/categorias/<int:pk>/', views.CategoriaDetailView.as_view(), name='categoria-detail'),

    # Proveedor
    path('api/proveedores/', views.ProveedorListCreateView.as_view(), name='proveedor-list-create'),
    path('api/proveedores/<int:pk>/', views.ProveedorDetailView.as_view(), name='proveedor-detail'),

    # Producto
    path('api/productos/', views.ProductoListCreateView.as_view(), name='producto-list-create'),
    path('api/productos/<int:pk>/', views.ProductoDetailView.as_view(), name='producto-detail'),

    # Pedido
    path('api/pedidos/', views.PedidoListCreateView.as_view(), name='pedido-list-create'),
    path('api/pedidos/<int:pk>/', views.PedidoDetailView.as_view(), name='pedido-detail'),

    # DetallePedido
    path('api/detallePedidos/', views.DetallePedidoListCreateView.as_view(), name='detallepedido-list-create'),
    path('api/detallePedidos/<int:pk>/', views.DetallePedidoDetailView.as_view(), name='detallepedido-detail'),

    # Venta
    path('api/ventas/', views.VentaListCreateView.as_view(), name='venta-list-create'),
    path('api/ventas/<int:pk>/', views.VentaDetailView.as_view(), name='venta-detail'),

    # DetalleVenta
    path('api/detalleVentas/', views.DetalleVentaListCreateView.as_view(), name='detalleventa-list-create'),
    path('api/detalleVentas/<int:pk>/', views.DetalleVentaDetailView.as_view(), name='detalleventa-detail'),

    # Código de verificación
    path('enviarCodigo/', views.EnviarCodigoGenericoView.as_view(), name='enviar_codigo'),
    path('validarCodigo/', views.ValidarCodigoView.as_view(), name='validar_codigo'),
    
]

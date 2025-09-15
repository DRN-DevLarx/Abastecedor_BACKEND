from django.urls import path
from . import views

urlpatterns = [
    # User
    path('users/', views.UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),

    # InformacionUsuario
    path('informacionUsuarios/', views.InformacionUsuarioListCreateView.as_view(), name='informacionusuario-list-create'),
    path('informacionUsuarios/<int:pk>/', views.InformacionUsuarioDetailView.as_view(), name='informacionusuario-detail'),

    path('asignarGrupo/', views.AsignarGrupoView.as_view(), name='asignargrupo'),

    # Categoria
    path('categorias/', views.CategoriaListCreateView.as_view(), name='categoria-list-create'),
    path('categorias/<int:pk>/', views.CategoriaDetailView.as_view(), name='categoria-detail'),

    # Proveedor
    path('proveedores/', views.ProveedorListCreateView.as_view(), name='proveedor-list-create'),
    path('proveedores/<int:pk>/', views.ProveedorDetailView.as_view(), name='proveedor-detail'),

    # Producto
    path('productos/', views.ProductoListCreateView.as_view(), name='producto-list-create'),
    path('productos/<int:pk>/', views.ProductoDetailView.as_view(), name='producto-detail'),

    # Pedido
    path('pedidos/', views.PedidoListCreateView.as_view(), name='pedido-list-create'),
    path('pedidos/<int:pk>/', views.PedidoDetailView.as_view(), name='pedido-detail'),

    # DetallePedido
    path('detallePedidos/', views.DetallePedidoListCreateView.as_view(), name='detallepedido-list-create'),
    path('detallePedidos/<int:pk>/', views.DetallePedidoDetailView.as_view(), name='detallepedido-detail'),

    # Venta
    path('ventas/', views.VentaListCreateView.as_view(), name='venta-list-create'),
    path('ventas/<int:pk>/', views.VentaDetailView.as_view(), name='venta-detail'),

    # DetalleVenta
    path('detalleVentas/', views.DetalleVentaListCreateView.as_view(), name='detalleventa-list-create'),
    path('detalleVentas/<int:pk>/', views.DetalleVentaDetailView.as_view(), name='detalleventa-detail'),

    # RegistroTemporal
    path('registroTemporal/', views.RegistroTemporalListCreateView.as_view(), name='detalleventa-list-create'),
    path('registroTemporal/<int:pk>/', views.RegistroTemporalDetailView.as_view(), name='registroTemporal-detail'),

    # Código de verificación
    path('enviarCodigo/', views.EnviarCodigoGenericoView.as_view(), name='enviar_codigo'),
    path('reenviarCodigo/', views.ReenviarCodigoView.as_view(), name='reenviar_codigo'),
    path('validarCodigo/', views.ValidarCodigoView.as_view(), name='validar_codigo'),
    
]

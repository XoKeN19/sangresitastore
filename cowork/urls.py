from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from eva_3 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.mostrarInicioPublico, name='inicio_publico'),
    path('login', views.mostrarLogin, name='login'),
    path('ingresar', views.insertarLogin, name='insertarLogin'),
    path('cerrar-sesion', views.cerrarSesion, name='cerrar_sesion'),
    path('registro', views.mostrarRegistro, name='registro'),
    path('crear-usuario', views.crearUsuario, name='crearUsuario'),
    path('inicio', views.mostrarInicio, name='inicio'),
    path('tienda', views.mostrarTienda, name='tienda'),
    path('coleccionables', views.mostrarColeccionables, name='coleccionables'),
    path('detalle-videojuego/<int:videojuego_id>', views.detalleVideojuego, name='detalle_videojuego'),
    path('detalle-coleccionable/<int:coleccionable_id>', views.detalleColeccionable, name='detalle_coleccionable'),
    path('agregar-carrito', views.agregarAlCarrito, name='agregar_carrito'),
    path('carrito', views.mostrarCarrito, name='carrito'),
    path('cambiar-cantidad-carrito', views.cambiarCantidadCarrito, name='cambiar_cantidad_carrito'),
    path('eliminar-carrito', views.eliminarDelCarrito, name='eliminar_carrito'),
    path('procesar-compra', views.procesarCompra, name='procesar_compra'),
    path('datos-retiro', views.mostrarDatosRetiro, name='datos_retiro'),
    path('procesar-datos-retiro', views.procesarDatosRetiro, name='procesar_datos_retiro'),
    path('confirmacion-retiro', views.mostrarConfirmacionRetiro, name='confirmacion_retiro'),
    path('admin-panel', views.mostrarAdminPanel, name='admin_panel'),
    path('gestionar-videojuego', views.gestionarVideojuego, name='gestionar_videojuego'),
    path('gestionar-coleccionable', views.gestionarColeccionable, name='gestionar_coleccionable'),
    path('editar-videojuego/<int:videojuego_id>', views.mostrarEditarVideojuego, name='editar_videojuego'),
    path('editar-coleccionable/<int:coleccionable_id>', views.mostrarEditarColeccionable, name='editar_coleccionable'),
    path('procesar-factura', views.procesarFactura, name='procesar_factura'),
    path('facturas-compras', views.mostrarFacturas, name='facturas_compras'),
    path('facturas-ventas', views.mostrarFacturasVentas, name='facturas_ventas'),
    path('detalle-factura/<int:factura_id>', views.detalleFactura, name='detalle_factura'),
    path('detalle-factura-compra/<int:factura_id>', views.detalleFacturaCompra, name='detalle_factura_compra'),
    path('estados-pedidos', views.estadosPedidos, name='estados_pedidos'),
    path('cambiar-estado-pedido/<int:pedido_id>', views.cambiarEstadoPedido, name='cambiar_estado_pedido'),
    path('cancelar-pedidos-vencidos', views.cancelarPedidosVencidos, name='cancelar_pedidos_vencidos'),
    path('gestionar-recomendados', views.gestionarRecomendados, name='gestionar_recomendados'),
    path('perfil', views.perfil, name='perfil'),
    path('actualizar-perfil', views.actualizarPerfil, name='actualizar_perfil'),
    path('cambiar-contrasena', views.cambiarContrasena, name='cambiar_contrasena'),
    path('mis-pedidos', views.misPedidos, name='mis_pedidos'),
    path('detalle-pedido/<int:pedido_id>', views.detallePedidoUsuario, name='detalle_pedido_usuario'),
    path('crear-superusuario', views.mostrarCrearSuperusuario, name='crear_superusuario'),
    path('procesar-superusuario', views.crearSuperusuario, name='procesar_superusuario'),
    path('listar-superusuarios', views.listarSuperusuarios, name='listar_superusuarios'),
    path('eliminar-superusuario/<int:usuario_id>', views.eliminarSuperusuario, name='eliminar_superusuario'),
]

# Configuración para servir archivos de medios en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

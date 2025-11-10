from django.contrib import admin
from .models import Usuario, Videojuego, TarjetaRegalo, Carrito, ItemCarrito, Pedido, FacturaCompra, FacturaVenta

# Register your models here.

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('numero_cliente', 'nombre', 'apellido', 'email', 'es_admin', 'is_owner', 'fecha_registro')
    list_filter = ('es_admin', 'is_owner', 'fecha_registro')
    search_fields = ('nombre', 'apellido', 'email', 'numero_cliente')
    readonly_fields = ('numero_cliente', 'fecha_registro')
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido', 'email', 'telefono', 'direccion')
        }),
        ('Información de Cliente', {
            'fields': ('numero_cliente', 'fecha_registro')
        }),
        ('Permisos', {
            'fields': ('es_admin', 'is_owner')
        }),
        ('Seguridad', {
            'fields': ('password',)
        }),
    )

@admin.register(Videojuego)
class VideojuegoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'plataforma', 'categoria', 'precio', 'stock', 'estado', 'es_recomendado', 'badge', 'fecha_creacion')
    list_filter = ('plataforma', 'categoria', 'estado', 'es_recomendado', 'badge', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion', 'plataforma', 'categoria')
    readonly_fields = ('fecha_creacion',)
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'precio', 'imagen')
        }),
        ('Categorización', {
            'fields': ('plataforma', 'categoria', 'badge')
        }),
        ('Inventario', {
            'fields': ('stock', 'estado')
        }),
        ('Recomendados', {
            'fields': ('es_recomendado', 'imagen_recomendada')
        }),
        ('Metadata', {
            'fields': ('fecha_creacion',)
        }),
    )

@admin.register(TarjetaRegalo)
class TarjetaRegaloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_tarjeta', 'categoria', 'precio', 'stock', 'estado', 'es_recomendado', 'badge', 'fecha_creacion')
    list_filter = ('tipo_tarjeta', 'categoria', 'estado', 'es_recomendado', 'badge', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion', 'tipo_tarjeta', 'categoria')
    readonly_fields = ('fecha_creacion',)
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'precio', 'imagen')
        }),
        ('Categorización', {
            'fields': ('tipo_tarjeta', 'categoria', 'badge'),
            'description': 'Tipo de Tarjeta de Regalo: Steam, PlayStation, Xbox, Nintendo, etc.'
        }),
        ('Inventario', {
            'fields': ('stock', 'estado')
        }),
        ('Recomendados', {
            'fields': ('es_recomendado', 'imagen_recomendada')
        }),
        ('Metadata', {
            'fields': ('fecha_creacion',)
        }),
    )

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha_creacion', 'activo')
    list_filter = ('activo', 'fecha_creacion')
    search_fields = ('usuario__nombre', 'usuario__apellido', 'usuario__email')
    readonly_fields = ('fecha_creacion',)

@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ('id', 'carrito', 'producto_info', 'cantidad', 'precio_unitario', 'precio_total')
    list_filter = ('carrito__activo',)
    search_fields = ('carrito__usuario__nombre', 'videojuego__nombre', 'tarjeta_regalo__nombre')
    
    def producto_info(self, obj):
        if obj.videojuego:
            return f"Videojuego: {obj.videojuego.nombre}"
        elif obj.tarjeta_regalo:
            return f"Tarjeta de Regalo: {obj.tarjeta_regalo.nombre}"
        return "Sin producto"
    producto_info.short_description = 'Producto'

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'total', 'estado', 'fecha_pedido', 'fecha_actualizacion', 'metodo_pago')
    list_filter = ('estado', 'metodo_pago', 'fecha_pedido', 'fecha_actualizacion')
    search_fields = ('usuario__nombre', 'usuario__apellido', 'usuario__email', 'numero_comprobante')
    readonly_fields = ('fecha_pedido', 'fecha_actualizacion')
    fieldsets = (
        ('Información del Pedido', {
            'fields': ('usuario', 'total', 'estado', 'metodo_pago', 'numero_comprobante')
        }),
        ('Dirección', {
            'fields': ('direccion_envio',)
        }),
        ('Fechas', {
            'fields': ('fecha_pedido', 'fecha_actualizacion')
        }),
    )

@admin.register(FacturaCompra)
class FacturaCompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_producto', 'proveedor', 'cantidad_comprada', 'precio_compra', 'total_factura', 'fecha_compra', 'producto_asociado')
    list_filter = ('proveedor', 'fecha_compra')
    search_fields = ('nombre_producto', 'proveedor', 'codigo_paquete', 'videojuego__nombre', 'tarjeta_regalo__nombre')
    readonly_fields = ('total_factura', 'fecha_compra')
    
    def producto_asociado(self, obj):
        if obj.videojuego:
            return f"Videojuego: {obj.videojuego.nombre}"
        elif obj.tarjeta_regalo:
            return f"Tarjeta de Regalo: {obj.tarjeta_regalo.nombre}"
        return "Sin asociar"
    producto_asociado.short_description = 'Producto Asociado'

@admin.register(FacturaVenta)
class FacturaVentaAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'usuario', 'pedido', 'subtotal', 'iva', 'total', 'estado', 'fecha_venta', 'metodo_pago')
    list_filter = ('estado', 'metodo_pago', 'fecha_venta')
    search_fields = ('numero_factura', 'usuario__nombre', 'usuario__apellido', 'usuario__email', 'pedido__id')
    readonly_fields = ('numero_factura', 'fecha_venta', 'subtotal', 'iva', 'total')
    fieldsets = (
        ('Información de la Factura', {
            'fields': ('numero_factura', 'usuario', 'pedido', 'estado')
        }),
        ('Totales', {
            'fields': ('subtotal', 'iva', 'total', 'metodo_pago')
        }),
        ('Observaciones', {
            'fields': ('observaciones',)
        }),
        ('Fecha', {
            'fields': ('fecha_venta',)
        }),
    )

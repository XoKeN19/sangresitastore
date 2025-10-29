from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, default='123')  # Contraseña por defecto
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    es_admin = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)  # Solo el propietario principal puede eliminar superusuarios
    fecha_registro = models.DateTimeField(auto_now_add=True)
    numero_cliente = models.CharField(max_length=10, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Generar número de cliente automáticamente si no existe
        if not self.numero_cliente:
            # Obtener el último número de cliente
            ultimo_usuario = Usuario.objects.filter(numero_cliente__isnull=False).order_by('-numero_cliente').first()
            if ultimo_usuario and ultimo_usuario.numero_cliente:
                try:
                    ultimo_numero = int(ultimo_usuario.numero_cliente)
                    self.numero_cliente = str(ultimo_numero + 1).zfill(6)
                except (ValueError, TypeError):
                    self.numero_cliente = "000001"
            else:
                self.numero_cliente = "000001"
        super().save(*args, **kwargs)
    
    def verificar_password(self, password_ingresado):
        """
        Verifica si el password ingresado coincide con el almacenado.
        Retorna True si coincide, False si no.
        """
        return self.password == password_ingresado
    
    def cambiar_password(self, password_nuevo):
        """
        Cambia el password del usuario.
        """
        self.password = password_nuevo
        self.save()

    def __str__(self):
        return f"{self.nombre} {self.apellido} - Cliente #{self.numero_cliente}"

class Videojuego(models.Model):
    BADGE_CHOICES = [
        ('best-seller', 'Más Vendido'),
        ('new-release', 'Nuevo Lanzamiento'),
        ('special-offer', 'Oferta Especial'),
        ('low-stock', 'A Punto de Irse'),
        ('', 'Sin Badge'),
    ]
    
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='videojuegos/', blank=True, null=True)
    plataforma = models.CharField(max_length=50)
    categoria = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)
    es_recomendado = models.BooleanField(default=False)
    badge = models.CharField(max_length=20, choices=BADGE_CHOICES, default='', blank=True)
    imagen_recomendada = models.ImageField(upload_to='recomendados/videojuegos/', blank=True, null=True, help_text="Imagen específica para mostrar en recomendados")
    estado = models.CharField(max_length=20, choices=[('disponible', 'Disponible'), ('agotado', 'Agotado')], default='disponible')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Coleccionable(models.Model):
    BADGE_CHOICES = [
        ('best-seller', 'Más Vendido'),
        ('new-release', 'Nuevo Lanzamiento'),
        ('special-offer', 'Oferta Especial'),
        ('low-stock', 'A Punto de Irse'),
        ('', 'Sin Badge'),
    ]
    
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='coleccionables/', blank=True, null=True)
    tipo_coleccionable = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)
    es_recomendado = models.BooleanField(default=False)
    badge = models.CharField(max_length=20, choices=BADGE_CHOICES, default='', blank=True)
    imagen_recomendada = models.ImageField(upload_to='recomendados/coleccionables/', blank=True, null=True, help_text="Imagen específica para mostrar en recomendados")
    estado = models.CharField(max_length=20, choices=[('disponible', 'Disponible'), ('agotado', 'Agotado')], default='disponible')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Carrito de {self.usuario}"

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    videojuego = models.ForeignKey(Videojuego, on_delete=models.CASCADE, null=True, blank=True)
    coleccionable = models.ForeignKey(Coleccionable, on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def precio_total(self):
        return self.cantidad * self.precio_unitario

    @property
    def producto(self):
        return self.videojuego if self.videojuego else self.coleccionable

    @property
    def tipo(self):
        return 'videojuego' if self.videojuego else 'coleccionable'

    def __str__(self):
        producto = self.videojuego if self.videojuego else self.coleccionable
        return f"{producto} - {self.cantidad} unidades"

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('realizado', 'Realizado'),
        ('cancelado', 'Cancelado'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    direccion_envio = models.TextField()
    metodo_pago = models.CharField(max_length=50, default='Transferencia')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    numero_comprobante = models.CharField(max_length=100, blank=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario} - {self.get_estado_display()}"
    
    def cancelar_pedido(self):
        """Cancela el pedido y devuelve los productos al stock"""
        if self.estado == 'pendiente':
            # Obtener el carrito asociado al pedido
            # Buscar el carrito desactivado más reciente del usuario ANTES de la fecha del pedido
            from datetime import timedelta
            
            # Buscar carritos desactivados antes de la fecha del pedido
            carrito = Carrito.objects.filter(
                usuario=self.usuario, 
                activo=False,
                fecha_creacion__lt=self.fecha_actualizacion
            ).order_by('-fecha_creacion').first()
            
            # Si no se encuentra uno antes, buscar el más reciente en general
            if not carrito:
                carrito = Carrito.objects.filter(
                    usuario=self.usuario, 
                    activo=False
                ).order_by('-fecha_creacion').first()
            
            if carrito:
                items = ItemCarrito.objects.filter(carrito=carrito)
                print(f"Cancelando pedido {self.id} - Carrito encontrado: {carrito.id}")
                print(f"Fecha del carrito: {carrito.fecha_creacion}")
                print(f"Items en el carrito: {items.count()}")
                
                for item in items:
                    if item.videojuego:
                        item.videojuego.stock += item.cantidad
                        # Cambiar estado a disponible si estaba agotado
                        if item.videojuego.estado == 'agotado' and item.videojuego.stock > 0:
                            item.videojuego.estado = 'disponible'
                        item.videojuego.save()
                        print(f"Devolviendo {item.cantidad} unidades de {item.videojuego.nombre} al stock (nuevo stock: {item.videojuego.stock})")
                    elif item.coleccionable:
                        item.coleccionable.stock += item.cantidad
                        # Cambiar estado a disponible si estaba agotado
                        if item.coleccionable.estado == 'agotado' and item.coleccionable.stock > 0:
                            item.coleccionable.estado = 'disponible'
                        item.coleccionable.save()
                        print(f"Devolviendo {item.cantidad} unidades de {item.coleccionable.nombre} al stock (nuevo stock: {item.coleccionable.stock})")
            else:
                print(f"No se encontró carrito para el pedido {self.id}")
            
            self.estado = 'cancelado'
            self.save()
            return True
        return False
    
    def marcar_realizado(self):
        """Marca el pedido como realizado"""
        if self.estado == 'pendiente':
            self.estado = 'realizado'
            self.save()
            return True
        return False

class FacturaCompra(models.Model):
    """Modelo para registrar las compras de productos al proveedor"""
    nombre_producto = models.CharField(max_length=200)
    cantidad_comprada = models.IntegerField()
    proveedor = models.CharField(max_length=200)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    videojuego = models.ForeignKey(Videojuego, on_delete=models.SET_NULL, null=True, blank=True)
    coleccionable = models.ForeignKey(Coleccionable, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    total_factura = models.DecimalField(max_digits=10, decimal_places=2)
    codigo_paquete = models.CharField(max_length=100, blank=True, help_text="Código de identificación del paquete o lote")
    observaciones = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # Calcular el total de la factura
        self.total_factura = self.cantidad_comprada * self.precio_compra
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Factura {self.id} - {self.nombre_producto} - {self.proveedor}"

class FacturaVenta(models.Model):
    """Modelo para registrar las ventas a clientes"""
    numero_factura = models.CharField(max_length=20, unique=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50, default='Retiro en Tienda')
    fecha_venta = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado')
    ], default='pendiente')
    observaciones = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # Los valores de subtotal, IVA y total ya vienen calculados correctamente desde la vista
        # No recalcular aquí para evitar duplicar el IVA
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Factura Venta {self.numero_factura} - {self.usuario.nombre} - ${self.total}"

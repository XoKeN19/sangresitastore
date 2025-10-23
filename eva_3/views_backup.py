from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Usuario, Videojuego, Coleccionable, Carrito, ItemCarrito, Pedido, FacturaCompra, FacturaVenta

def mostrarLogin(request):
    return render(request,'login.html')

def insertarLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            usuario = Usuario.objects.get(email=email)
            # Verificar contraseña del usuario
            if password == usuario.password:
                # Asegurar que la sesión esté activa
                if not request.session.session_key:
                    request.session.create()
                
                # Establecer datos de sesión
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nombre'] = usuario.nombre
                request.session['es_admin'] = usuario.es_admin
                
                # Forzar guardado de la sesión
                request.session.save()
                
                if usuario.es_admin:
                    return redirect('admin_panel')
                else:
                    return redirect('inicio_publico')
            else:
                messages.error(request, 'Contraseña incorrecta')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')
    
    return render(request, 'login.html')

def cerrarSesion(request):
    """Cerrar sesión del usuario"""
    # Limpiar datos de sesión específicos
    if 'usuario_id' in request.session:
        del request.session['usuario_id']
    if 'usuario_nombre' in request.session:
        del request.session['usuario_nombre']
    if 'es_admin' in request.session:
        del request.session['es_admin']
    
    # Limpiar toda la sesión
    request.session.flush()
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('inicio_publico')

def mostrarRegistro(request):
    return render(request, 'registro.html')

def crearUsuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        password = request.POST.get('password')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        
        try:
            usuario = Usuario.objects.create(
                nombre=nombre,
                apellido=apellido,
                email=email,
                password=password,
                telefono=telefono,
                direccion=direccion
            )
            messages.success(request, 'Usuario creado exitosamente')
            return redirect('login')
        except Exception as e:
            messages.error(request, 'Error al crear usuario')
    
    return render(request, 'registro.html')

def mostrarInicioPublico(request):
    """Página inicial pública sin requerir login"""
    # Solo mostrar productos recomendados que estén disponibles
    videojuegos_recomendados = Videojuego.objects.filter(es_recomendado=True, estado='disponible')[:3]
    coleccionables_destacados = Coleccionable.objects.filter(estado='disponible')[:3]
    
    # Asegurar que la sesión esté activa
    if not request.session.session_key:
        request.session.create()
    
    # Obtener información de la sesión
    usuario_nombre = request.session.get('usuario_nombre', None)
    es_admin = request.session.get('es_admin', False)
    
    context = {
        'videojuegos_recomendados': videojuegos_recomendados,
        'coleccionables_destacados': coleccionables_destacados,
        'usuario_nombre': usuario_nombre,
        'es_admin': es_admin
    }
    return render(request, 'inicio.html', context)

def mostrarInicio(request):
    """Página inicial para usuarios logueados"""
    if 'usuario_id' not in request.session:
        return redirect('inicio_publico')
    
    # Solo mostrar productos recomendados que estén disponibles
    videojuegos_recomendados = Videojuego.objects.filter(es_recomendado=True, estado='disponible')[:3]
    coleccionables_destacados = Coleccionable.objects.filter(estado='disponible')[:3]
    
    context = {
        'videojuegos_recomendados': videojuegos_recomendados,
        'coleccionables_destacados': coleccionables_destacados
    }
    return render(request, 'inicio.html', context)

def mostrarTienda(request):
    # Solo mostrar productos disponibles
    videojuegos = Videojuego.objects.filter(estado='disponible')
    orden = request.GET.get('orden', 'nombre')
    
    if orden == 'precio_asc':
        videojuegos = videojuegos.order_by('precio')
    elif orden == 'precio_desc':
        videojuegos = videojuegos.order_by('-precio')
    
    context = {
        'videojuegos': videojuegos, 
        'orden': orden,
        'usuario_nombre': request.session.get('usuario_nombre', None),
        'es_admin': request.session.get('es_admin', False)
    }
    return render(request, 'tienda.html', context)

def mostrarColeccionables(request):
    # Solo mostrar productos disponibles
    coleccionables = Coleccionable.objects.filter(estado='disponible')
    orden = request.GET.get('orden', 'nombre')
    
    if orden == 'precio_asc':
        coleccionables = coleccionables.order_by('precio')
    elif orden == 'precio_desc':
        coleccionables = coleccionables.order_by('-precio')
    
    context = {
        'coleccionables': coleccionables, 
        'orden': orden,
        'usuario_nombre': request.session.get('usuario_nombre', None),
        'es_admin': request.session.get('es_admin', False)
    }
    return render(request, 'coleccionables.html', context)

def detalleVideojuego(request, videojuego_id):
    videojuego = get_object_or_404(Videojuego, id=videojuego_id)
    return render(request, 'detalle_videojuego.html', {'videojuego': videojuego})

def detalleColeccionable(request, coleccionable_id):
    coleccionable = get_object_or_404(Coleccionable, id=coleccionable_id)
    return render(request, 'detalle_coleccionable.html', {'coleccionable': coleccionable})

def agregarAlCarrito(request):
    if request.method == 'POST':
        if 'usuario_id' not in request.session:
            messages.error(request, 'Debes iniciar sesión para agregar productos al carrito')
            return redirect('login')
        
        usuario = get_object_or_404(Usuario, id=request.session['usuario_id'])
        producto_id = request.POST.get('producto_id')
        producto_tipo = request.POST.get('tipo')  # 'videojuego' o 'coleccionable'
        cantidad = int(request.POST.get('cantidad', 1))
        
        carrito, created = Carrito.objects.get_or_create(usuario=usuario, activo=True)
        
        if producto_tipo == 'videojuego':
            producto = get_object_or_404(Videojuego, id=producto_id)
            
            # Verificar stock disponible
            if producto.stock < cantidad:
                messages.error(request, f'No hay suficiente stock. Disponible: {producto.stock}')
                return redirect('detalle_videojuego', videojuego_id=producto_id)
            
            # Buscar si ya existe en el carrito
            try:
                item = ItemCarrito.objects.get(carrito=carrito, videojuego=producto)
                # Verificar si al agregar más cantidad no excede el stock
                if item.cantidad + cantidad > producto.stock:
                    messages.error(request, f'No puedes agregar más cantidad. Stock disponible: {producto.stock}')
                    return redirect('detalle_videojuego', videojuego_id=producto_id)
                item.cantidad += cantidad
                item.save()
            except ItemCarrito.DoesNotExist:
                ItemCarrito.objects.create(
                    carrito=carrito,
                    videojuego=producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio
                )
            
            # Restar del stock
            producto.stock -= cantidad
            producto.save()
            
            messages.success(request, f'{cantidad} unidad(es) de {producto.nombre} agregada(s) al carrito')
    
    else:
        producto = get_object_or_404(Coleccionable, id=producto_id)
        
        # Verificar stock disponible
        if producto.stock < cantidad:
            messages.error(request, f'No hay suficiente stock. Disponible: {producto.stock}')
            return redirect('detalle_coleccionable', coleccionable_id=producto_id)
        
        # Buscar si ya existe en el carrito
        try:
            item = ItemCarrito.objects.get(carrito=carrito, coleccionable=producto)
            # Verificar si al agregar más cantidad no excede el stock
            if item.cantidad + cantidad > producto.stock:
                messages.error(request, f'No puedes agregar más cantidad. Stock disponible: {producto.stock}')
                return redirect('detalle_coleccionable', coleccionable_id=producto_id)
            item.cantidad += cantidad
            item.save()
        except ItemCarrito.DoesNotExist:
            ItemCarrito.objects.create(
                carrito=carrito,
                coleccionable=producto,
                cantidad=cantidad,
                precio_unitario=producto.precio
            )
        
        # Restar del stock
        producto.stock -= cantidad
        producto.save()
        
        messages.success(request, f'{cantidad} unidad(es) de {producto.nombre} agregada(s) al carrito')
    
    # Redirigir según el tipo de producto
    if producto_tipo == 'videojuego':
        return redirect('detalle_videojuego', videojuego_id=producto_id)
    else:
        return redirect('detalle_coleccionable', coleccionable_id=producto_id)
    
    return redirect('inicio')

def cambiarCantidadCarrito(request):
    if request.method == 'POST':
        if 'usuario_id' not in request.session:
            return redirect('login')
        
        item_id = request.POST.get('item_id')
        nueva_cantidad = int(request.POST.get('nueva_cantidad', 1))
        
        try:
            item = ItemCarrito.objects.get(id=item_id)
            producto = item.videojuego if item.videojuego else item.coleccionable
            
            if nueva_cantidad <= 0:
                # Eliminar item del carrito y devolver stock
                producto.stock += item.cantidad
                producto.save()
                item.delete()
                messages.success(request, 'Producto eliminado del carrito')
            else:
                diferencia = nueva_cantidad - item.cantidad
                
                if diferencia > 0:  # Agregar más
                    if producto.stock >= diferencia:
                        producto.stock -= diferencia
                        producto.save()
                        item.cantidad = nueva_cantidad
                        item.save()
                        messages.success(request, 'Cantidad actualizada')
                    else:
                        messages.error(request, f'No hay suficiente stock. Disponible: {producto.stock}')
                else:  # Quitar cantidad
                    producto.stock += abs(diferencia)
                    producto.save()
                    item.cantidad = nueva_cantidad
                    item.save()
                    messages.success(request, 'Cantidad actualizada')
        
        except ItemCarrito.DoesNotExist:
            messages.error(request, 'Item no encontrado')
    
    return redirect('carrito')

def eliminarDelCarrito(request):
    if request.method == 'POST':
        if 'usuario_id' not in request.session:
            return redirect('login')
        
        item_id = request.POST.get('item_id')
        
        try:
            item = ItemCarrito.objects.get(id=item_id)
            producto = item.videojuego if item.videojuego else item.coleccionable
            
            # Devolver stock
            producto.stock += item.cantidad
            producto.save()
            
            # Eliminar item
            item.delete()
            messages.success(request, 'Producto eliminado del carrito')
        
        except ItemCarrito.DoesNotExist:
            messages.error(request, 'Item no encontrado')
    
    return redirect('carrito')

def mostrarCarrito(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    usuario = get_object_or_404(Usuario, id=request.session['usuario_id'])
    carrito = Carrito.objects.filter(usuario=usuario, activo=True).first()
    items = []
    total = 0
    
    if carrito:
        items = ItemCarrito.objects.filter(carrito=carrito)
        # Calcular subtotal para cada item
        for item in items:
            item.subtotal = item.cantidad * item.precio_unitario
        total = sum(item.subtotal for item in items)
    
    context = {'items': items, 'total': total}
    return render(request, 'carrito.html', context)

def procesarCompra(request):
    if request.method == 'POST':
        if 'usuario_id' not in request.session:
            return redirect('login')
        
        usuario = get_object_or_404(Usuario, id=request.session['usuario_id'])
        carrito = Carrito.objects.filter(usuario=usuario, activo=True).first()
        
        if not carrito:
            messages.error(request, 'No hay productos en el carrito')
            return redirect('carrito')
        
        items = ItemCarrito.objects.filter(carrito=carrito)
        
        if not items.exists():
            messages.error(request, 'No hay productos en el carrito')
            return redirect('carrito')
        
        total = sum(item.cantidad * item.precio_unitario for item in items)
        
        # Guardar datos del carrito en la sesión para el formulario de retiro
        request.session['carrito_compra'] = {
            'items': [
                {
                    'producto_id': item.videojuego.id if item.videojuego else item.coleccionable.id,
                    'producto_tipo': 'videojuego' if item.videojuego else 'coleccionable',
                    'producto_nombre': item.videojuego.nombre if item.videojuego else item.coleccionable.nombre,
                    'cantidad': item.cantidad,
                    'precio_unitario': float(item.precio_unitario),
                    'subtotal': float(item.cantidad * item.precio_unitario)
                }
                for item in items
            ],
            'total': float(total),
            'carrito_id': carrito.id
        }
        
        return redirect('datos_retiro')
    
    return redirect('carrito')

def mostrarDatosRetiro(request):
    """Mostrar formulario para datos de retiro en tienda"""
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    if 'carrito_compra' not in request.session:
        messages.error(request, 'No hay datos de compra disponibles')
        return redirect('carrito')
    
    usuario = get_object_or_404(Usuario, id=request.session['usuario_id'])
    carrito_data = request.session['carrito_compra']
    
    context = {
        'usuario': usuario,
        'items': carrito_data['items'],
        'total': carrito_data['total'],
        'usuario_nombre': request.session.get('usuario_nombre', None),
        'es_admin': request.session.get('es_admin', False)
    }
    return render(request, 'datos_retiro.html', context)

def procesarDatosRetiro(request):
    """Procesar datos de retiro y crear el pedido"""
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    if 'carrito_compra' not in request.session:
        messages.error(request, 'No hay datos de compra disponibles')
        return redirect('carrito')
    
    if request.method == 'POST':
        try:
            usuario = get_object_or_404(Usuario, id=request.session['usuario_id'])
            carrito_data = request.session['carrito_compra']
            
            # Obtener datos del formulario
            nombre_completo = request.POST.get('nombre_completo')
            telefono = request.POST.get('telefono')
            email = request.POST.get('email')
            observaciones = request.POST.get('observaciones', '')
            
            # Asegurar que el usuario tenga número de cliente
            usuario.save()  # Esto generará el número de cliente automáticamente
            
            # Calcular totales con IVA (descontado)
            subtotal = carrito_data['total']
            iva = subtotal * 0.19
            total_con_iva = subtotal - iva  # IVA descontado
            
            # Crear pedido
            pedido = Pedido.objects.create(
                usuario=usuario,
                total=total_con_iva,
                direccion_envio=f"Retiro en tienda - {nombre_completo} - {telefono}",
                metodo_pago='Retiro en Tienda'
            )
            
            # Crear factura de venta
            factura_venta = FacturaVenta.objects.create(
                numero_factura=f"FV-{pedido.id:06d}",
                usuario=usuario,
                pedido=pedido,
                subtotal=subtotal,
                iva=iva,
                total=total_con_iva,
                metodo_pago='Retiro en Tienda',
                estado='pendiente',
                observaciones=observaciones
            )
            
            # Desactivar carrito
            carrito = Carrito.objects.get(id=carrito_data['carrito_id'])
            carrito.activo = False
            carrito.save()
            
            # Guardar datos en sesión para la confirmación
            request.session['pedido_completado'] = {
                'pedido_id': pedido.id,
                'factura_id': factura_venta.id,
                'numero_factura': factura_venta.numero_factura,
                'numero_cliente': usuario.numero_cliente,
                'nombre_completo': nombre_completo,
                'telefono': telefono,
                'email': email,
                'subtotal': float(subtotal),
                'iva': float(iva),
                'total': float(total_con_iva),
                'observaciones': observaciones
            }
            
            # Limpiar datos de compra
            del request.session['carrito_compra']
            
            return redirect('confirmacion_retiro')
            
        except Exception as e:
            messages.error(request, f'Error al procesar el pedido: {str(e)}')
            return redirect('datos_retiro')
    
    return redirect('datos_retiro')

def mostrarConfirmacionRetiro(request):
    """Mostrar confirmación final del pedido"""
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    if 'pedido_completado' not in request.session:
        messages.error(request, 'No hay pedido completado')
        return redirect('carrito')
    
    pedido_data = request.session['pedido_completado']
    
    context = {
        'pedido_data': pedido_data,
        'usuario_nombre': request.session.get('usuario_nombre', None),
        'es_admin': request.session.get('es_admin', False)
    }
    return render(request, 'confirmacion_retiro.html', context)

def mostrarAdminPanel(request):
    if 'usuario_id' not in request.session or not request.session.get('es_admin'):
        return redirect('login')
    
    videojuegos = Videojuego.objects.all()
    coleccionables = Coleccionable.objects.all()
    facturas_compras = FacturaCompra.objects.all().order_by('-fecha_compra')[:10]  # Últimas 10 facturas de compra
    facturas_ventas = FacturaVenta.objects.all().order_by('-fecha_venta')[:10]  # Últimas 10 facturas de venta
    
    context = {
        'videojuegos': videojuegos,
        'coleccionables': coleccionables,
        'facturas': facturas_compras,
        'facturas_ventas': facturas_ventas
    }
    return render(request, 'admin_panel.html', context)

def gestionarVideojuego(request):
    if 'usuario_id' not in request.session or not request.session.get('es_admin'):
        return redirect('login')
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'crear':
            Videojuego.objects.create(
                nombre=request.POST.get('nombre'),
                descripcion=request.POST.get('descripcion'),
                precio=request.POST.get('precio'),
                plataforma=request.POST.get('plataforma'),
                categoria=request.POST.get('categoria'),
                stock=int(request.POST.get('stock', 0)),
                es_recomendado=request.POST.get('es_recomendado') == 'on',
                estado=request.POST.get('estado', 'disponible')
            )
        elif accion == 'eliminar':
            videojuego_id = request.POST.get('videojuego_id')
            Videojuego.objects.filter(id=videojuego_id).delete()
        elif accion == 'editar':
            videojuego_id = request.POST.get('videojuego_id')
            videojuego = Videojuego.objects.get(id=videojuego_id)
            videojuego.nombre = request.POST.get('nombre')
            videojuego.descripcion = request.POST.get('descripcion')
            videojuego.precio = request.POST.get('precio')
            videojuego.plataforma = request.POST.get('plataforma')
            videojuego.categoria = request.POST.get('categoria')
            videojuego.stock = int(request.POST.get('stock', 0))
            videojuego.es_recomendado = request.POST.get('es_recomendado') == 'on'
            videojuego.estado = request.POST.get('estado', 'disponible')
            
            # Manejar imagen si se proporciona una nueva
            if 'imagen' in request.FILES and request.FILES['imagen']:
                videojuego.imagen = request.FILES['imagen']
            
            videojuego.save()
    
    return redirect('admin_panel')

def mostrarEditarVideojuego(request, videojuego_id):
    if 'usuario_id' not in request.session or not request.session.get('es_admin'):
        return redirect('login')
    
    videojuego = get_object_or_404(Videojuego, id=videojuego_id)
    return render(request, 'editar_videojuego.html', {'videojuego': videojuego})

def mostrarEditarColeccionable(request, coleccionable_id):
    if 'usuario_id' not in request.session or not request.session.get('es_admin'):
        return redirect('login')
    
    coleccionable = get_object_or_404(Coleccionable, id=coleccionable_id)
    return render(request, 'editar_coleccionable.html', {'coleccionable': coleccionable})

def gestionarColeccionable(request):
    if 'usuario_id' not in request.session or not request.session.get('es_admin'):
        return redirect('login')
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'crear':
            Coleccionable.objects.create(
                nombre=request.POST.get('nombre'),
                descripcion=request.POST.get('descripcion'),
                precio=request.POST.get('precio'),
                tipo_coleccionable=request.POST.get('tipo_coleccionable'),
                categoria=request.POST.get('categoria'),
                stock=int(request.POST.get('stock', 0)),
                estado=request.POST.get('estado', 'disponible')
            )
        elif accion == 'eliminar':
            coleccionable_id = request.POST.get('coleccionable_id')
            Coleccionable.objects.filter(id=coleccionable_id).delete()
        elif accion == 'editar':
            coleccionable_id = request.POST.get('coleccionable_id')
            coleccionable = Coleccionable.objects.get(id=coleccionable_id)
            coleccionable.nombre = request.POST.get('nombre')
            coleccionable.descripcion = request.POST.get('descripcion')
            coleccionable.precio = request.POST.get('precio')
            coleccionable.tipo_coleccionable = request.POST.get('tipo_coleccionable')
            coleccionable.categoria = request.POST.get('categoria')
            coleccionable.stock = int(request.POST.get('stock', 0))
            coleccionable.estado = request.POST.get('estado', 'disponible')
            
            # Manejar imagen si se proporciona una nueva
            if 'imagen' in request.FILES and request.FILES['imagen']:
                coleccionable.imagen = request.FILES['imagen']
            
            coleccionable.save()
    
    return redirect('admin_panel')

def procesarFactura(request):
    """Procesar factura de compra y agregar stock al producto"""
    if 'usuario_id' not in request.session or not request.session.get('es_admin'):
        return redirect('login')
    
    if request.method == 'POST':
        try:
            producto_id = request.POST.get('producto_id')
            producto_tipo = request.POST.get('producto_tipo')
            nombre_producto = request.POST.get('nombre_producto')
            cantidad_comprada = int(request.POST.get('cantidad_comprada'))
            proveedor = request.POST.get('proveedor')
            precio_compra = float(request.POST.get('precio_compra'))
            observaciones = request.POST.get('observaciones', '')
            es_formulario_creacion = request.POST.get('es_formulario_creacion') == 'true'
            stock_inicial_formulario = int(request.POST.get('stock_inicial_formulario', 0))
            
            # Verificar si es un formulario de creación (sin producto_id)
            if es_formulario_creacion:
                # En formularios de creación, solo crear la factura sin asociar producto
                factura = FacturaCompra.objects.create(
                    nombre_producto=nombre_producto,
                    cantidad_comprada=cantidad_comprada,
                    proveedor=proveedor,
                    precio_compra=precio_compra,
                    observaciones=observaciones + f" [Stock inicial: {stock_inicial_formulario + cantidad_comprada} unidades]"
                )
                
                messages.success(request, f'Factura #{factura.id} registrada para {nombre_producto}. Total de stock a agregar: {stock_inicial_formulario + cantidad_comprada} unidades.')
            else:
                # Obtener el producto existente
                if producto_tipo == 'videojuego':
                    producto = get_object_or_404(Videojuego, id=producto_id)
                else:
                    producto = get_object_or_404(Coleccionable, id=producto_id)
                
                # Crear la factura de compra
                factura = FacturaCompra.objects.create(
                    nombre_producto=nombre_producto,
                    cantidad_comprada=cantidad_comprada,
                    proveedor=proveedor,
                    precio_compra=precio_compra,
                    observaciones=observaciones
                )
                
                # Asociar el producto a la factura
                if producto_tipo == 'videojuego':
                    factura.videojuego = producto
                else:
                    factura.coleccionable = producto
                factura.save()
                
                # Agregar stock al producto
                producto.stock += cantidad_comprada
                producto.save()
                
                messages.success(request, f'Se agregaron {cantidad_comprada} unidades al stock de {producto.nombre}. Factura #{factura.id} registrada.')
            
        except Exception as e:
            messages.error(request, f'Error al procesar la factura: {str(e)}')
    
    return redirect('admin_panel')

def mostrarFacturas(request):
    """Mostrar todas las facturas de compras"""
    if 'usuario_id' not in request.session or not request.session.get('es_admin'):
        return redirect('login')
    
    facturas = FacturaCompra.objects.all().order_by('-fecha_compra')
    
    context = {
        'facturas': facturas,
        'usuario_nombre': request.session.get('usuario_nombre', None),
        'es_admin': request.session.get('es_admin', False)
    }
    return render(request, 'facturas_compras.html', context)

def detallesFactura(request, factura_id):
    """Mostrar detalles de una factura específica"""
    if 'usuario_id' not in request.session or not request.session.get('es_admin'):
        return redirect('login')
    
    factura = get_object_or_404(FacturaCompra, id=factura_id)
    
    context = {
        'factura': factura
    }
    return render(request, 'detalles_factura.html', context)

def detallesFacturaVenta(request, factura_id):
    """Mostrar detalles de una factura de venta"""
    if 'usuario_id' not in request.session or not request.session.get('es_admin'):
        return redirect('login')
    
    factura = get_object_or_404(FacturaVenta, id=factura_id)
    
    # Obtener items del pedido (simulados desde los datos del carrito)
    # Como no tenemos ItemPedido, vamos a simular los datos
    items_pedido = []
    
    context = {
        'factura': factura,
        'items_pedido': items_pedido
    }
    return render(request, 'detalles_factura_venta.html', context)


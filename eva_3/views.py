from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.messages import constants
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
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
    # Mostrar 4 productos recomendados para que se vean las 4 cards
    videojuegos_recomendados = Videojuego.objects.filter(es_recomendado=True, estado='disponible')[:4]
    coleccionables_destacados = Coleccionable.objects.filter(estado='disponible')[:4]
    
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
    
    # Mostrar 4 productos recomendados para que se vean las 4 cards
    videojuegos_recomendados = Videojuego.objects.filter(es_recomendado=True, estado='disponible')[:4]
    coleccionables_destacados = Coleccionable.objects.filter(estado='disponible')[:4]
    
    context = {
        'videojuegos_recomendados': videojuegos_recomendados,
        'coleccionables_destacados': coleccionables_destacados
    }
    return render(request, 'inicio.html', context)

def mostrarTienda(request):
    # Mostrar todos los productos (disponibles y agotados)
    videojuegos = Videojuego.objects.all()
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
    # Mostrar todos los productos (disponibles y agotados)
    coleccionables = Coleccionable.objects.all()
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
    context = {
        'videojuego': videojuego,
        'usuario_nombre': request.session.get('usuario_nombre', None),
        'es_admin': request.session.get('es_admin', False)
    }
    return render(request, 'detalle_videojuego.html', context)

def detalleColeccionable(request, coleccionable_id):
    coleccionable = get_object_or_404(Coleccionable, id=coleccionable_id)
    context = {
        'coleccionable': coleccionable,
        'usuario_nombre': request.session.get('usuario_nombre', None),
        'es_admin': request.session.get('es_admin', False)
    }
    return render(request, 'detalle_coleccionable.html', context)

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
            
            # Cambiar estado a agotado si stock llega a 0
            if producto.stock <= 0:
                producto.stock = 0
                producto.estado = 'agotado'
            
            producto.save()
            
            messages.success(request, f'{cantidad} unidad(es) de {producto.nombre} agregada(s) al carrito')
            return redirect('detalle_videojuego', videojuego_id=producto_id)
    
    elif producto_tipo == 'coleccionable':
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
                
                # Cambiar estado a disponible si el stock es mayor a 0
                if producto.stock > 0 and producto.estado == 'agotado':
                    producto.estado = 'disponible'
                
                producto.save()
                item.delete()
                messages.success(request, 'Producto eliminado del carrito')
            else:
                diferencia = nueva_cantidad - item.cantidad
                
                if diferencia > 0:  # Agregar más
                    if producto.stock >= diferencia:
                        producto.stock -= diferencia
                        
                        # Cambiar estado a agotado si stock llega a 0
                        if producto.stock <= 0:
                            producto.stock = 0
                            producto.estado = 'agotado'
                        
                        producto.save()
                        item.cantidad = nueva_cantidad
                        item.save()
                        messages.success(request, 'Cantidad actualizada')
                    else:
                        messages.error(request, f'No hay suficiente stock. Disponible: {producto.stock}')
                else:  # Quitar cantidad
                    producto.stock += abs(diferencia)
                    
                    # Cambiar estado a disponible si el stock es mayor a 0
                    if producto.stock > 0 and producto.estado == 'agotado':
                        producto.estado = 'disponible'
                    
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
            
            # Cambiar estado a disponible si el stock es mayor a 0
            if producto.stock > 0 and producto.estado == 'agotado':
                producto.estado = 'disponible'
            
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
        total = sum(item.precio_total for item in items)
    
    context = {
        'items': items, 
        'total': total,
        'usuario_nombre': request.session.get('usuario_nombre', None),
        'es_admin': request.session.get('es_admin', False)
    }
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
            direccion = request.POST.get('direccion', '')
            observaciones = request.POST.get('observaciones', '')
            
            # Asegurar que el usuario tenga número de cliente
            usuario.save()  # Esto generará el número de cliente automáticamente
            
            # Calcular totales correctamente
            # El precio en los productos YA incluye IVA
            total_con_iva = carrito_data['total']  # Este es el precio final que ya incluye IVA
            subtotal = total_con_iva / 1.19  # Precio sin IVA
            iva = total_con_iva - subtotal  # IVA es la diferencia
            
            # Crear pedido
            pedido = Pedido.objects.create(
                usuario=usuario,
                total=total_con_iva,
                direccion_envio=f"Retiro en tienda - {nombre_completo} - {telefono} - {direccion}",
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
                'direccion': direccion,
                'subtotal': float(subtotal),
                'iva': float(iva),
                'total': float(total_con_iva),
                'observaciones': observaciones,
                'fecha_pedido': pedido.fecha_pedido.strftime('%d/%m/%Y %H:%M')
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
    
    from django.core.paginator import Paginator
    from django.db.models import Q
    
    # Obtener parámetros de filtrado y búsqueda
    busqueda = request.GET.get('busqueda', '')
    tipo_filtro = request.GET.get('tipo', '')
    estado_filtro = request.GET.get('estado', '')
    orden = request.GET.get('orden', 'nombre')
    pagina = request.GET.get('pagina', 1)
    
    # Configuración de paginación
    PRODUCTOS_POR_PAGINA = 10
    
    # Filtrar videojuegos
    videojuegos = Videojuego.objects.all()
    if busqueda:
        videojuegos = videojuegos.filter(
            Q(nombre__icontains=busqueda) | 
            Q(descripcion__icontains=busqueda) |
            Q(plataforma__icontains=busqueda) |
            Q(categoria__icontains=busqueda)
        )
    if estado_filtro:
        videojuegos = videojuegos.filter(estado=estado_filtro)
    
    # Aplicar ordenamiento
    if orden == 'nombre':
        videojuegos = videojuegos.order_by('nombre')
    elif orden == 'precio_asc':
        videojuegos = videojuegos.order_by('precio')
    elif orden == 'precio_desc':
        videojuegos = videojuegos.order_by('-precio')
    elif orden == 'stock_asc':
        videojuegos = videojuegos.order_by('stock')
    elif orden == 'stock_desc':
        videojuegos = videojuegos.order_by('-stock')
    elif orden == 'fecha_desc':
        videojuegos = videojuegos.order_by('-id')
    
    # Paginar videojuegos
    paginator_videojuegos = Paginator(videojuegos, PRODUCTOS_POR_PAGINA)
    videojuegos_paginados = paginator_videojuegos.get_page(pagina)
    
    # Filtrar coleccionables
    coleccionables = Coleccionable.objects.all()
    if busqueda:
        coleccionables = coleccionables.filter(
            Q(nombre__icontains=busqueda) | 
            Q(descripcion__icontains=busqueda) |
            Q(tipo_coleccionable__icontains=busqueda) |
            Q(categoria__icontains=busqueda)
        )
    if estado_filtro:
        coleccionables = coleccionables.filter(estado=estado_filtro)
    
    # Aplicar ordenamiento
    if orden == 'nombre':
        coleccionables = coleccionables.order_by('nombre')
    elif orden == 'precio_asc':
        coleccionables = coleccionables.order_by('precio')
    elif orden == 'precio_desc':
        coleccionables = coleccionables.order_by('-precio')
    elif orden == 'stock_asc':
        coleccionables = coleccionables.order_by('stock')
    elif orden == 'stock_desc':
        coleccionables = coleccionables.order_by('-stock')
    elif orden == 'fecha_desc':
        coleccionables = coleccionables.order_by('-id')
    
    # Paginar coleccionables
    paginator_coleccionables = Paginator(coleccionables, PRODUCTOS_POR_PAGINA)
    coleccionables_paginados = paginator_coleccionables.get_page(pagina)
    
    # Obtener todos los productos para estadísticas (sin filtros)
    videojuegos_todos = Videojuego.objects.all()
    coleccionables_todos = Coleccionable.objects.all()
    
    # Estadísticas generales
    total_videojuegos = videojuegos_todos.count()
    total_coleccionables = coleccionables_todos.count()
    total_productos = total_videojuegos + total_coleccionables
    
    # Estadísticas de stock
    videojuegos_sin_stock = videojuegos_todos.filter(stock=0).count()
    coleccionables_sin_stock = coleccionables_todos.filter(stock=0).count()
    total_sin_stock = videojuegos_sin_stock + coleccionables_sin_stock
    
    # Obtener facturas (sin paginación para el resumen)
    facturas_compras = FacturaCompra.objects.all().order_by('-fecha_compra')[:5]  # Solo las últimas 5
    facturas_ventas = FacturaVenta.objects.all().order_by('-fecha_venta')[:5]  # Solo las últimas 5
    facturas_compras_count = FacturaCompra.objects.count()
    facturas_ventas_count = FacturaVenta.objects.count()
    
    # Estadísticas de pedidos
    total_pedidos = Pedido.objects.count()
    pendientes = Pedido.objects.filter(estado='pendiente').count()
    realizados = Pedido.objects.filter(estado='realizado').count()
    cancelados = Pedido.objects.filter(estado='cancelado').count()
    
    # Obtener categorías únicas para filtros
    categorias_videojuegos = Videojuego.objects.values_list('categoria', flat=True).distinct().exclude(categoria__isnull=True).exclude(categoria='')
    categorias_coleccionables = Coleccionable.objects.values_list('categoria', flat=True).distinct().exclude(categoria__isnull=True).exclude(categoria='')
    categorias_unicas = sorted(set(list(categorias_videojuegos) + list(categorias_coleccionables)))
    
    context = {
        'videojuegos': videojuegos_paginados,
        'coleccionables': coleccionables_paginados,
        'facturas': facturas_compras,
        'facturas_compras_count': facturas_compras_count,
        'facturas_ventas_count': facturas_ventas_count,
        'facturas_ventas': facturas_ventas,
        'total_pedidos': total_pedidos,
        'pendientes': pendientes,
        'realizados': realizados,
        'cancelados': cancelados,
        # Nuevos datos para filtros y estadísticas
        'busqueda': busqueda,
        'tipo_filtro': tipo_filtro,
        'estado_filtro': estado_filtro,
        'orden': orden,
        'categorias': categorias_unicas,
        'total_videojuegos': total_videojuegos,
        'total_coleccionables': total_coleccionables,
        'total_productos': total_productos,
        'total_sin_stock': total_sin_stock,
        'videojuegos_sin_stock': videojuegos_sin_stock,
        'coleccionables_sin_stock': coleccionables_sin_stock,
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
                
                messages.add_message(request, constants.SUCCESS, f'Factura #{factura.id} registrada para {nombre_producto}. Total de stock a agregar: {stock_inicial_formulario + cantidad_comprada} unidades.', extra_tags='admin')
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
                
                # Obtener código de paquete si existe
                codigo_paquete = request.POST.get('codigo_paquete', '')
                if codigo_paquete:
                    factura.codigo_paquete = codigo_paquete
                
                factura.save()
                
                # Agregar stock al producto
                producto.stock += cantidad_comprada
                
                # Cambiar estado a disponible si el stock es mayor a 0 y estaba agotado
                if producto.stock > 0 and producto.estado == 'agotado':
                    producto.estado = 'disponible'
                
                producto.save()
                
                messages.add_message(request, constants.SUCCESS, f'Se agregaron {cantidad_comprada} unidades al stock de {producto.nombre}. Factura #{factura.id} registrada.', extra_tags='admin')
            
        except Exception as e:
            messages.add_message(request, constants.ERROR, f'Error al procesar la factura: {str(e)}', extra_tags='admin')
    
    return redirect('admin_panel')

def mostrarFacturas(request):
    """Mostrar todas las facturas de compras"""
    if 'usuario_id' not in request.session or not request.session.get('es_admin'):
        return redirect('login')
    
    facturas = FacturaCompra.objects.all().order_by('-fecha_compra')
    
    # Filtrar por ID de factura si se especifica
    numero_busqueda = request.GET.get('numero', '')
    if numero_busqueda:
        try:
            numero = int(numero_busqueda)
            facturas = facturas.filter(id=numero)
        except ValueError:
            # Si no es un número válido, no filtrar nada
            pass
    
    context = {
        'facturas': facturas,
        'numero_busqueda': numero_busqueda,
        'usuario_nombre': request.session.get('usuario_nombre', None),
        'es_admin': request.session.get('es_admin', False)
    }
    return render(request, 'facturas_compras.html', context)


def mostrarFacturasVentas(request):
    """Mostrar todas las facturas de ventas"""
    if 'usuario_id' not in request.session or not request.session.get('es_admin'):
        return redirect('login')
    
    facturas = FacturaVenta.objects.all().order_by('-fecha_venta')
    
    # Filtrar por número de factura si se especifica
    numero_busqueda = request.GET.get('numero', '')
    if numero_busqueda:
        # Buscar por número de factura (ej: FV-000021 o solo 21)
        if numero_busqueda.startswith('FV-'):
            facturas = facturas.filter(numero_factura=numero_busqueda)
        else:
            # Si solo se ingresa un número, buscar por número de factura que termine con ese número
            try:
                numero = int(numero_busqueda)
                facturas = facturas.filter(numero_factura__endswith=f'-{numero:06d}')
            except ValueError:
                # Si no es un número válido, buscar como texto
                facturas = facturas.filter(numero_factura__icontains=numero_busqueda)
    
    context = {
        'facturas': facturas,
        'numero_busqueda': numero_busqueda,
        'usuario_nombre': request.session.get('usuario_nombre', None),
        'es_admin': request.session.get('es_admin', False)
    }
    return render(request, 'facturas_ventas.html', context)


def detalleFactura(request, factura_id):
    """Mostrar detalle completo de una factura de venta"""
    if 'usuario_id' not in request.session or not request.session.get('es_admin'):
        return redirect('login')
    
    factura = get_object_or_404(FacturaVenta, id=factura_id)
    
    # Obtener el pedido asociado a la factura
    # La factura tiene una relación directa con el pedido
    pedido = factura.pedido
    
    # Obtener los items del carrito desactivado que se usó para crear el pedido
    # El carrito se desactiva cuando se crea el pedido, pero los items se mantienen
    carrito_usado = Carrito.objects.filter(
        usuario=factura.usuario, 
        activo=False,
        fecha_creacion__lte=factura.fecha_venta
    ).order_by('-fecha_creacion').first()
    
    items_pedido = []
    if carrito_usado:
        items_pedido = ItemCarrito.objects.filter(carrito=carrito_usado)
    
    context = {
        'factura': factura,
        'pedido': pedido,
        'items_pedido': items_pedido,
        'usuario_nombre': request.session.get('usuario_nombre', None),
        'es_admin': request.session.get('es_admin', False)
    }
    return render(request, 'detalle_factura.html', context)


def detalleFacturaCompra(request, factura_id):
    """Mostrar detalle completo de una factura de compra"""
    if 'usuario_id' not in request.session or not request.session.get('es_admin'):
        return redirect('login')
    
    factura = get_object_or_404(FacturaCompra, id=factura_id)
    
    context = {
        'factura': factura,
        'usuario_nombre': request.session.get('usuario_nombre', None),
        'es_admin': request.session.get('es_admin', False)
    }
    return render(request, 'detalle_factura_compra.html', context)


def estadosPedidos(request):
    """Mostrar todos los pedidos con sus estados para gestión administrativa"""
    if 'usuario_id' not in request.session or not request.session.get('es_admin'):
        return redirect('login')
    
    # Obtener todos los pedidos ordenados por fecha
    pedidos = Pedido.objects.all().order_by('-fecha_pedido')
    
    # Filtrar por estado si se especifica
    estado_filtro = request.GET.get('estado', '')
    if estado_filtro:
        pedidos = pedidos.filter(estado=estado_filtro)
    
    # Filtrar por ID si se especifica
    id_busqueda = request.GET.get('id', '')
    if id_busqueda:
        try:
            id_numero = int(id_busqueda)
            pedidos = pedidos.filter(id=id_numero)
        except ValueError:
            # Si no es un número válido, no filtrar por ID
            pass
    
    # Estadísticas
    total_pedidos = Pedido.objects.count()
    pendientes = Pedido.objects.filter(estado='pendiente').count()
    realizados = Pedido.objects.filter(estado='realizado').count()
    cancelados = Pedido.objects.filter(estado='cancelado').count()
    
    context = {
        'pedidos': pedidos,
        'total_pedidos': total_pedidos,
        'pendientes': pendientes,
        'realizados': realizados,
        'cancelados': cancelados,
        'estado_filtro': estado_filtro,
        'id_busqueda': id_busqueda,
        'usuario_nombre': request.session.get('usuario_nombre', None),
        'es_admin': request.session.get('es_admin', False)
    }
    return render(request, 'estados_pedidos.html', context)


def cambiarEstadoPedido(request, pedido_id):
    """Cambiar el estado de un pedido específico"""
    if 'usuario_id' not in request.session or not request.session.get('es_admin'):
        return redirect('login')
    
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id)
        nueva_accion = request.POST.get('accion')
        
        if nueva_accion == 'realizado':
            if pedido.marcar_realizado():
                messages.add_message(request, constants.SUCCESS, f'Pedido #{pedido.id} marcado como realizado.', extra_tags='admin')
            else:
                messages.add_message(request, constants.ERROR, f'No se pudo marcar el pedido #{pedido.id} como realizado.', extra_tags='admin')
        
        elif nueva_accion == 'cancelado':
            if pedido.cancelar_pedido():
                messages.add_message(request, constants.SUCCESS, f'Pedido #{pedido.id} cancelado y stock restaurado.', extra_tags='admin')
            else:
                messages.add_message(request, constants.ERROR, f'No se pudo cancelar el pedido #{pedido.id}.', extra_tags='admin')
        
        return redirect('estados_pedidos')
    
    return redirect('estados_pedidos')


def cancelarPedidosVencidos(request):
    """Cancelar automáticamente pedidos pendientes de más de 1 semana"""
    if 'usuario_id' not in request.session or not request.session.get('es_admin'):
        return redirect('login')
    
    from datetime import datetime, timedelta
    from django.utils import timezone
    
    # Calcular fecha límite (1 semana atrás)
    fecha_limite = timezone.now() - timedelta(days=7)
    
    # Obtener pedidos pendientes de más de 1 semana
    pedidos_vencidos = Pedido.objects.filter(
        estado='pendiente',
        fecha_pedido__lt=fecha_limite
    )
    
    cancelados_count = 0
    for pedido in pedidos_vencidos:
        if pedido.cancelar_pedido():
            cancelados_count += 1
    
    return redirect('estados_pedidos')

def gestionarRecomendados(request):
    """Gestionar productos recomendados para el inicio"""
    if 'usuario_id' not in request.session or not request.session.get('es_admin'):
        return redirect('login')
    
    # Obtener todos los productos disponibles
    videojuegos = Videojuego.objects.filter(estado='disponible').order_by('nombre')
    coleccionables = Coleccionable.objects.filter(estado='disponible').order_by('nombre')
    
    # Obtener productos recomendados actuales
    videojuegos_recomendados = Videojuego.objects.filter(es_recomendado=True).order_by('id')
    coleccionables_recomendados = Coleccionable.objects.filter(es_recomendado=True).order_by('id')
    
    if request.method == 'POST':
        # Procesar cambios en videojuegos recomendados
        videojuegos_ids = request.POST.getlist('videojuegos_recomendados')
        badges_videojuegos = {}
        
        for videojuego_id in videojuegos_ids:
            badge_key = f'badge_videojuego_{videojuego_id}'
            if badge_key in request.POST:
                badges_videojuegos[videojuego_id] = request.POST[badge_key]
        
        # Limpiar recomendados anteriores
        Videojuego.objects.update(es_recomendado=False)
        
        # Marcar nuevos recomendados
        for videojuego_id in videojuegos_ids:
            try:
                videojuego = Videojuego.objects.get(id=videojuego_id)
                videojuego.es_recomendado = True
                if videojuego_id in badges_videojuegos:
                    videojuego.badge = badges_videojuegos[videojuego_id]
                
                # Procesar imagen recomendada
                imagen_key = f'imagen_videojuego_{videojuego_id}'
                if imagen_key in request.FILES:
                    videojuego.imagen_recomendada = request.FILES[imagen_key]
                
                videojuego.save()
            except Videojuego.DoesNotExist:
                pass
        
        # Procesar cambios en coleccionables recomendados
        coleccionables_ids = request.POST.getlist('coleccionables_recomendados')
        badges_coleccionables = {}
        
        for coleccionable_id in coleccionables_ids:
            badge_key = f'badge_coleccionable_{coleccionable_id}'
            if badge_key in request.POST:
                badges_coleccionables[coleccionable_id] = request.POST[badge_key]
        
        # Limpiar recomendados anteriores de coleccionables
        Coleccionable.objects.update(es_recomendado=False)
        
        # Marcar nuevos coleccionables recomendados
        for coleccionable_id in coleccionables_ids:
            try:
                coleccionable = Coleccionable.objects.get(id=coleccionable_id)
                coleccionable.es_recomendado = True
                if coleccionable_id in badges_coleccionables:
                    coleccionable.badge = badges_coleccionables[coleccionable_id]
                
                # Procesar imagen recomendada
                imagen_key = f'imagen_coleccionable_{coleccionable_id}'
                if imagen_key in request.FILES:
                    coleccionable.imagen_recomendada = request.FILES[imagen_key]
                
                coleccionable.save()
            except Coleccionable.DoesNotExist:
                pass
        
        messages.add_message(request, constants.SUCCESS, 'Productos recomendados actualizados correctamente.', extra_tags='admin')
        return redirect('gestionar_recomendados')
    
    context = {
        'videojuegos': videojuegos,
        'coleccionables': coleccionables,
        'videojuegos_recomendados': videojuegos_recomendados,
        'coleccionables_recomendados': coleccionables_recomendados,
        'usuario_nombre': request.session.get('usuario_nombre', None),
        'es_admin': request.session.get('es_admin', False)
    }
    return render(request, 'gestionar_recomendados.html', context)

def misPedidos(request):
    """Mostrar los pedidos del usuario actual"""
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    usuario = get_object_or_404(Usuario, id=request.session['usuario_id'])
    
    # Obtener todos los pedidos del usuario ordenados por fecha (más recientes primero)
    pedidos = Pedido.objects.filter(usuario=usuario).order_by('-fecha_pedido')
    
    # Calcular días restantes para cada pedido pendiente
    pedidos_con_tiempo = []
    for pedido in pedidos:
        pedido_dict = {
            'pedido': pedido,
            'dias_restantes': None
        }
        
        if pedido.estado == 'pendiente':
            # Calcular cuántos días han pasado desde la fecha del pedido
            if pedido.fecha_pedido:
                if timezone.is_aware(pedido.fecha_pedido):
                    ahora = timezone.now()
                else:
                    ahora = datetime.now()
                
                dias_transcurridos = (ahora - pedido.fecha_pedido).days
                dias_restantes = 7 - dias_transcurridos
                
                # Si ya pasaron más de 7 días, mostrar 0
                pedido_dict['dias_restantes'] = max(0, dias_restantes)
        
        pedidos_con_tiempo.append(pedido_dict)
    
    context = {
        'pedidos_con_tiempo': pedidos_con_tiempo,
        'usuario': usuario,
        'usuario_nombre': request.session.get('usuario_nombre', None),
        'es_admin': request.session.get('es_admin', False)
    }
    return render(request, 'mis_pedidos.html', context)

def detallePedidoUsuario(request, pedido_id):
    """Mostrar el detalle de un pedido específico del usuario"""
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    usuario = get_object_or_404(Usuario, id=request.session['usuario_id'])
    
    # Obtener el pedido y verificar que pertenece al usuario actual
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=usuario)
    
    # Calcular días restantes si el pedido está pendiente
    dias_restantes = None
    if pedido.estado == 'pendiente' and pedido.fecha_pedido:
        if timezone.is_aware(pedido.fecha_pedido):
            ahora = timezone.now()
        else:
            ahora = datetime.now()
        
        dias_transcurridos = (ahora - pedido.fecha_pedido).days
        dias_restantes = max(0, 7 - dias_transcurridos)
    
    # Obtener la factura de venta asociada
    try:
        factura = FacturaVenta.objects.get(pedido=pedido)
    except FacturaVenta.DoesNotExist:
        factura = None
    
    # Obtener los items del carrito asociado al pedido
    carrito = Carrito.objects.filter(
        usuario=usuario,
        activo=False,
        fecha_creacion__lte=pedido.fecha_pedido
    ).order_by('-fecha_creacion').first()
    
    items = []
    if carrito:
        items = ItemCarrito.objects.filter(carrito=carrito)
    
    context = {
        'pedido': pedido,
        'factura': factura,
        'items': items,
        'dias_restantes': dias_restantes,
        'usuario': usuario,
        'usuario_nombre': request.session.get('usuario_nombre', None),
        'es_admin': request.session.get('es_admin', False)
    }
    return render(request, 'detalle_pedido_usuario.html', context)

def perfil(request):
    """Vista para mostrar y editar el perfil del usuario"""
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    usuario = get_object_or_404(Usuario, id=request.session['usuario_id'])
    
    context = {
        'usuario': usuario,
        'usuario_nombre': request.session.get('usuario_nombre', None),
        'es_admin': request.session.get('es_admin', False)
    }
    return render(request, 'perfil.html', context)

def actualizarPerfil(request):
    """Vista para actualizar los datos del perfil del usuario"""
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        usuario = get_object_or_404(Usuario, id=request.session['usuario_id'])
        
        # Obtener datos del formulario
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        
        # Actualizar datos básicos
        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.telefono = telefono
        usuario.direccion = direccion
        usuario.save()
        
        # Actualizar nombre en sesión
        request.session['usuario_nombre'] = nombre
        
        messages.success(request, 'Perfil actualizado correctamente')
        return redirect('perfil')
    
    return redirect('perfil')

def cambiarContrasena(request):
    """Vista para cambiar la contraseña del usuario"""
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        usuario = get_object_or_404(Usuario, id=request.session['usuario_id'])
        
        # Obtener contraseñas del formulario
        contrasena_actual = request.POST.get('contrasena_actual')
        nueva_contrasena = request.POST.get('nueva_contrasena')
        confirmar_contrasena = request.POST.get('confirmar_contrasena')
        
        # Validar contraseña actual
        if usuario.contrasena != contrasena_actual:
            messages.error(request, 'La contraseña actual es incorrecta')
            return redirect('perfil')
        
        # Validar que las nuevas contraseñas coincidan
        if nueva_contrasena != confirmar_contrasena:
            messages.error(request, 'Las nuevas contraseñas no coinciden')
            return redirect('perfil')
        
        # Validar longitud mínima
        if len(nueva_contrasena) < 6:
            messages.error(request, 'La nueva contraseña debe tener al menos 6 caracteres')
            return redirect('perfil')
        
        # Actualizar contraseña
        usuario.contrasena = nueva_contrasena
        usuario.save()
        
        messages.success(request, 'Contraseña cambiada correctamente')
        return redirect('perfil')
    
    return redirect('perfil')


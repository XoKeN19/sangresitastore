from django.core.management.base import BaseCommand
from eva_3.models import ItemCarrito, Videojuego, TarjetaRegalo


class Command(BaseCommand):
    help = 'Elimina productos no disponibles de todos los carritos de usuarios'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Muestra qué se eliminaría sin eliminar realmente',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('MODO DRY-RUN: No se eliminará nada, solo se mostrará qué se eliminaría'))
        
        # Obtener todos los items del carrito
        items = ItemCarrito.objects.all()
        items_eliminados = 0
        items_problema = []
        
        for item in items:
            producto_existe = False
            problema = None
            
            # Verificar si es un videojuego
            if item.videojuego_id:
                try:
                    videojuego = Videojuego.objects.get(id=item.videojuego_id)
                    producto_existe = True
                except Videojuego.DoesNotExist:
                    problema = f"Videojuego con ID {item.videojuego_id} no existe"
            # Verificar si es una tarjeta de regalo
            elif item.tarjeta_regalo_id:
                try:
                    tarjeta = TarjetaRegalo.objects.get(id=item.tarjeta_regalo_id)
                    producto_existe = True
                except TarjetaRegalo.DoesNotExist:
                    problema = f"Tarjeta de Regalo con ID {item.tarjeta_regalo_id} no existe"
            # Si no tiene ni videojuego ni tarjeta_regalo
            else:
                problema = "Item sin producto asociado (ambos campos son None)"
            
            # Si hay un problema, agregar a la lista para eliminar
            if problema:
                items_problema.append({
                    'item': item,
                    'problema': problema
                })
        
        # Mostrar resumen
        self.stdout.write(f'\nTotal de items en carritos: {items.count()}')
        self.stdout.write(f'Items con problemas encontrados: {len(items_problema)}')
        
        if items_problema:
            self.stdout.write('\nItems que serán eliminados:')
            for item_info in items_problema:
                item = item_info['item']
                usuario = item.carrito.usuario if item.carrito else "Sin usuario"
                self.stdout.write(
                    f'  - Item ID {item.id}: {item_info["problema"]} '
                    f'(Usuario: {usuario}, Carrito ID: {item.carrito.id if item.carrito else "N/A"})'
                )
            
            if not dry_run:
                # Eliminar los items con problemas
                for item_info in items_problema:
                    item = item_info['item']
                    item.delete()
                    items_eliminados += 1
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\nSe eliminaron {items_eliminados} items del carrito con productos no disponibles.'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'\nEn modo DRY-RUN: Se eliminarían {len(items_problema)} items.'
                    )
                )
        else:
            self.stdout.write(self.style.SUCCESS('\nNo se encontraron items con productos no disponibles.'))
        
        # También verificar items donde ambos campos son None
        items_sin_producto = ItemCarrito.objects.filter(videojuego__isnull=True, tarjeta_regalo__isnull=True)
        if items_sin_producto.exists():
            self.stdout.write(f'\nItems sin producto (ambos campos None): {items_sin_producto.count()}')
            if not dry_run:
                count = items_sin_producto.count()
                items_sin_producto.delete()
                items_eliminados += count
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Se eliminaron {count} items adicionales sin producto.'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'En modo DRY-RUN: Se eliminarían {items_sin_producto.count()} items adicionales sin producto.'
                    )
                )


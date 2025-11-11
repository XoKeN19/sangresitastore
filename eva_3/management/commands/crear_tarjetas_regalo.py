"""
Comando de Django para crear 5 tarjetas de regalo adicionales
"""
from django.core.management.base import BaseCommand
from eva_3.models import TarjetaRegalo


class Command(BaseCommand):
    help = 'Crea 5 tarjetas de regalo adicionales'

    def handle(self, *args, **options):
        tarjetas_data = [
            {
                'nombre': 'Tarjeta de Regalo Steam $50 USD',
                'descripcion': 'Tarjeta de regalo digital de Steam con valor de $50 USD. Perfecta para comprar juegos, DLCs y contenido adicional en la plataforma Steam. Código digital entregado instantáneamente.',
                'precio': 50000.00,
                'tipo_tarjeta': 'Steam',
                'categoria': 'Videojuegos',
                'stock': 25,
                'estado': 'disponible',
                'badge': 'best-seller',
            },
            {
                'nombre': 'Tarjeta de Regalo PlayStation Store $30 USD',
                'descripcion': 'Tarjeta de regalo digital de PlayStation Store con valor de $30 USD. Ideal para comprar juegos, contenido descargable y suscripciones de PlayStation Plus. Disponible para PS4 y PS5.',
                'precio': 30000.00,
                'tipo_tarjeta': 'PlayStation',
                'categoria': 'Videojuegos',
                'stock': 20,
                'estado': 'disponible',
                'badge': 'new-release',
            },
            {
                'nombre': 'Tarjeta de Regalo Xbox $25 USD',
                'descripcion': 'Tarjeta de regalo digital de Xbox con valor de $25 USD. Perfecta para comprar juegos, Game Pass, contenido adicional y suscripciones en Xbox One y Xbox Series X/S.',
                'precio': 25000.00,
                'tipo_tarjeta': 'Xbox',
                'categoria': 'Videojuegos',
                'stock': 18,
                'estado': 'disponible',
                'badge': 'special-offer',
            },
            {
                'nombre': 'Tarjeta de Regalo Nintendo eShop $20 USD',
                'descripcion': 'Tarjeta de regalo digital de Nintendo eShop con valor de $20 USD. Ideal para comprar juegos, DLCs y contenido adicional en Nintendo Switch. Código digital válido para todas las regiones.',
                'precio': 20000.00,
                'tipo_tarjeta': 'Nintendo',
                'categoria': 'Videojuegos',
                'stock': 15,
                'estado': 'disponible',
                'badge': '',
            },
            {
                'nombre': 'Tarjeta de Regalo Epic Games $15 USD',
                'descripcion': 'Tarjeta de regalo digital de Epic Games Store con valor de $15 USD. Perfecta para comprar juegos exclusivos, V-Bucks de Fortnite y contenido adicional en la plataforma Epic Games.',
                'precio': 15000.00,
                'tipo_tarjeta': 'Epic Games',
                'categoria': 'Videojuegos',
                'stock': 12,
                'estado': 'disponible',
                'badge': 'new-release',
            },
        ]

        creadas = 0
        for tarjeta_data in tarjetas_data:
            # Verificar si ya existe una tarjeta con el mismo nombre
            if not TarjetaRegalo.objects.filter(nombre=tarjeta_data['nombre']).exists():
                TarjetaRegalo.objects.create(**tarjeta_data)
                creadas += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Tarjeta creada: {tarjeta_data["nombre"]}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Tarjeta ya existe: {tarjeta_data["nombre"]}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nTotal de tarjetas creadas: {creadas} de {len(tarjetas_data)}')
        )


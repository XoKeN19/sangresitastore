"""
Script para actualizar las descripciones de tarjetas de regalo
"""
from django.core.management.base import BaseCommand
from eva_3.models import TarjetaRegalo


class Command(BaseCommand):
    help = 'Actualiza las descripciones de tarjetas de regalo'

    def handle(self, *args, **options):
        tarjetas_regalo = TarjetaRegalo.objects.all()
        actualizados = 0
        
        for tarjeta_regalo in tarjetas_regalo:
            # Si la descripción no parece ser de tarjeta de regalo, actualizarla
            descripcion_original = tarjeta_regalo.descripcion.lower()
            
            # Verificar si ya tiene formato de tarjeta de regalo
            if any(palabra in descripcion_original for palabra in ['tarjeta', 'regalo', 'gift card', 'steam', 'playstation', 'xbox', 'nintendo']):
                self.stdout.write(
                    self.style.WARNING(f'Tarjeta de regalo "{tarjeta_regalo.nombre}" ya tiene descripción correcta')
                )
                continue
            
            # Crear nueva descripción basada en el tipo
            tipo = tarjeta_regalo.tipo_tarjeta.lower()
            nueva_descripcion = f"Tarjeta de regalo {tarjeta_regalo.tipo_tarjeta} con un valor de ${tarjeta_regalo.precio}. "
            nueva_descripcion += f"Perfecta para regalar a tus seres queridos. Puedes canjearla en la plataforma correspondiente. "
            nueva_descripcion += f"Categoría: {tarjeta_regalo.categoria}."
            
            tarjeta_regalo.descripcion = nueva_descripcion
            tarjeta_regalo.save()
            actualizados += 1
            
            self.stdout.write(
                self.style.SUCCESS(f'Actualizado: {tarjeta_regalo.nombre}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nTotal de tarjetas de regalo actualizadas: {actualizados}')
        )


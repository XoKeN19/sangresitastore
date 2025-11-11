from django.core.management.base import BaseCommand
from eva_3.models import Usuario


class Command(BaseCommand):
    help = 'Actualiza usuarios de Sangresita Store a Re:Connect y sus correos electrónicos'

    def handle(self, *args, **options):
        # Buscar usuarios con "sangresita" en el nombre, apellido o email
        usuarios_actualizados = 0
        
        # Buscar por nombre
        usuarios_nombre = Usuario.objects.filter(nombre__icontains='sangresita')
        for usuario in usuarios_nombre:
            usuario.nombre = usuario.nombre.replace('Sangresita', 'Re:Connect').replace('sangresita', 'Re:Connect')
            if '@sangresita' in usuario.email.lower() or 'sangresita' in usuario.email.lower():
                # Actualizar email
                nuevo_email = usuario.email.lower().replace('@sangresita', '@reconnect.cl').replace('sangresita', 'reconnect').replace('@reconnectstore.cl', '@reconnect.cl')
                # Verificar si el nuevo email ya existe
                if not Usuario.objects.filter(email=nuevo_email).exclude(id=usuario.id).exists():
                    usuario.email = nuevo_email
                else:
                    self.stdout.write(
                        self.style.WARNING(f'El email {nuevo_email} ya existe. No se actualizó el email de {usuario.nombre} {usuario.apellido}')
                    )
            usuario.save()
            usuarios_actualizados += 1
            self.stdout.write(
                self.style.SUCCESS(f'Usuario actualizado: {usuario.nombre} {usuario.apellido} - {usuario.email}')
            )
        
        # Buscar por apellido
        usuarios_apellido = Usuario.objects.filter(apellido__icontains='sangresita')
        for usuario in usuarios_apellido:
            usuario.apellido = usuario.apellido.replace('Sangresita', 'Re:Connect').replace('sangresita', 'Re:Connect')
            if '@sangresita' in usuario.email.lower() or 'sangresita' in usuario.email.lower():
                nuevo_email = usuario.email.lower().replace('@sangresita', '@reconnect.cl').replace('sangresita', 'reconnect').replace('@reconnectstore.cl', '@reconnect.cl')
                if not Usuario.objects.filter(email=nuevo_email).exclude(id=usuario.id).exists():
                    usuario.email = nuevo_email
                else:
                    self.stdout.write(
                        self.style.WARNING(f'El email {nuevo_email} ya existe. No se actualizó el email de {usuario.nombre} {usuario.apellido}')
                    )
            usuario.save()
            usuarios_actualizados += 1
            self.stdout.write(
                self.style.SUCCESS(f'Usuario actualizado: {usuario.nombre} {usuario.apellido} - {usuario.email}')
            )
        
        # Buscar por email
        usuarios_email = Usuario.objects.filter(email__icontains='sangresita')
        for usuario in usuarios_email:
            nuevo_email = usuario.email.lower().replace('@sangresita', '@reconnect.cl').replace('sangresita', 'reconnect').replace('@reconnectstore.cl', '@reconnect.cl')
            if not Usuario.objects.filter(email=nuevo_email).exclude(id=usuario.id).exists():
                usuario.email = nuevo_email
                usuario.save()
                usuarios_actualizados += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Email actualizado: {usuario.nombre} {usuario.apellido} - {usuario.email}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'El email {nuevo_email} ya existe. No se actualizó el email de {usuario.nombre} {usuario.apellido}')
                )
        
        # También actualizar usuarios con @reconnectstore.cl a @reconnect.cl
        usuarios_reconnectstore = Usuario.objects.filter(email__icontains='@reconnectstore.cl')
        for usuario in usuarios_reconnectstore:
            nuevo_email = usuario.email.lower().replace('@reconnectstore.cl', '@reconnect.cl')
            if not Usuario.objects.filter(email=nuevo_email).exclude(id=usuario.id).exists():
                usuario.email = nuevo_email
                usuario.save()
                usuarios_actualizados += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Email actualizado: {usuario.nombre} {usuario.apellido} - {usuario.email}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'El email {nuevo_email} ya existe. No se actualizó el email de {usuario.nombre} {usuario.apellido}')
                )
        
        if usuarios_actualizados == 0:
            self.stdout.write(
                self.style.SUCCESS('No se encontraron usuarios con referencias a "Sangresita Store"')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'\nTotal de usuarios actualizados: {usuarios_actualizados}')
            )


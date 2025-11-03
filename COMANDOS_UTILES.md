# 🛠️ Comandos Útiles Post-Deploy

Comandos que necesitarás después de desplegar en Render.

---

## 📡 Comandos desde Render Shell

Para ejecutar estos comandos:
1. Ve a tu Web Service en Render
2. Click en "Shell" en el menú izquierdo
3. Espera a que cargue la terminal
4. Ejecuta los comandos

### Crear Superusuario
```bash
python manage.py createsuperuser
```

### Aplicar Migraciones
```bash
python manage.py migrate
```

### Recolectar Archivos Estáticos
```bash
python manage.py collectstatic --no-input
```

### Ver Usuarios
```bash
python manage.py shell
>>> from eva_3.models import Usuario
>>> Usuario.objects.all()
>>> exit()
```

### Crear Datos de Prueba
```bash
python manage.py shell
>>> from eva_3.models import Videojuego, Coleccionable
>>> # Crea tus objetos aquí
>>> exit()
```

### Ver Información de la Base de Datos
```bash
python manage.py dbshell
\dt  # Listar tablas
\q   # Salir
```

---

## 💻 Comandos Git Locales

### Ver Estado
```bash
git status
```

### Agregar Cambios
```bash
git add .
# o archivos específicos:
git add cowork/settings.py
git add eva_3/views.py
```

### Hacer Commit
```bash
git commit -m "Descripción clara del cambio"
```

### Subir Cambios
```bash
git push
```

### Ver Historial
```bash
git log --oneline
```

### Ver Diferencias
```bash
git diff
```

### Crear Nueva Rama
```bash
git checkout -b nombre-rama
```

### Cambiar de Rama
```bash
git checkout main
```

### Ver Ramas
```bash
git branch
```

---

## 🔍 Comandos de Verificación Local

### Verificar Proyecto
```bash
python verificar_proyecto.py
```

### Correr Servidor Local
```bash
python manage.py runserver
```

### Verificar Migraciones
```bash
python manage.py showmigrations
```

### Crear Migraciones
```bash
python manage.py makemigrations
```

### Verificar Configuración
```bash
python manage.py check
```

### Verificar Deploy Settings
```bash
python manage.py check --deploy
```

---

## 📦 Comandos de Dependencias

### Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Actualizar Dependencias
```bash
pip install --upgrade django
pip freeze > requirements.txt
```

### Ver Dependencias Instaladas
```bash
pip list
```

### Crear Entorno Virtual (si no lo tienes)
```bash
python -m venv venv
```

### Activar Entorno Virtual
Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

---

## 🗄️ Comandos de Base de Datos

### Backup de Base de Datos (Local)
```bash
python manage.py dumpdata > backup.json
```

### Restaurar Base de Datos (Local)
```bash
python manage.py loaddata backup.json
```

### Backup de Datos Específicos
```bash
python manage.py dumpdata eva_3.Videojuego > videojuegos.json
python manage.py dumpdata eva_3.Coleccionable > coleccionables.json
```

### Limpiar Base de Datos (¡Cuidado!)
```bash
python manage.py flush
```

---

## 🔐 Comandos de Seguridad

### Generar Nueva SECRET_KEY
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Cambiar Password de Usuario (en Shell)
```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='admin')
>>> user.set_password('nueva_password')
>>> user.save()
>>> exit()
```

---

## 📊 Comandos de Mantenimiento en Render

### Ver Logs en Tiempo Real
En Render:
1. Ve a tu Web Service
2. Click en "Logs"
3. Selecciona "Live Logs"

### Reiniciar Servicio
En Render:
1. Ve a tu Web Service
2. Click en "Manual Deploy"
3. Click en "Deploy latest commit"

### Ver Uso de Recursos
En Render:
1. Ve a tu Web Service
2. Click en "Metrics"

---

## 🐛 Debug y Solución de Problemas

### Ver Logs Completos (Render)
```bash
# Los logs se ven automáticamente en la interfaz de Render
# Para búsqueda específica, usa Ctrl+F en los logs
```

### Verificar Variables de Entorno (Render Shell)
```bash
echo $SECRET_KEY
echo $DEBUG
echo $DATABASE_URL
```

### Probar Conexión a DB (Render Shell)
```bash
python manage.py dbshell
```

### Ver Configuración Actual (Render Shell)
```bash
python manage.py diffsettings
```

---

## 📝 Comandos de Contenido

### Crear Usuario desde Shell
```python
python manage.py shell
>>> from eva_3.models import Usuario
>>> usuario = Usuario.objects.create(
...     nombre="Juan",
...     apellido="Pérez",
...     email="juan@example.com",
...     numero_cliente="123456"
... )
>>> usuario.save()
>>> exit()
```

### Listar Videojuegos
```python
python manage.py shell
>>> from eva_3.models import Videojuego
>>> for v in Videojuego.objects.all():
...     print(v.nombre, v.precio)
>>> exit()
```

---

## 🔄 Workflow Típico de Actualización

```bash
# 1. Hacer cambios en tu código local

# 2. Probar localmente
python manage.py runserver

# 3. Si funciona, hacer commit
git add .
git commit -m "Descripción del cambio"

# 4. Subir a GitHub
git push

# 5. Render detecta y redespliega automáticamente

# 6. Verificar en la URL de producción
# https://tu-app.onrender.com

# 7. Si hay problemas, revisar logs en Render
```

---

## 📚 Recursos

- **Django Management Commands**: https://docs.djangoproject.com/en/4.1/ref/django-admin/
- **Git Commands**: https://git-scm.com/docs
- **Render Docs**: https://render.com/docs

---

## 💡 Tips

1. **Siempre prueba localmente antes de hacer push**
2. **Usa commits descriptivos**: `git commit -m "Fix: Corrige error en carrito"`
3. **Revisa los logs** si algo falla en producción
4. **Haz backups** de tu base de datos regularmente
5. **Documenta cambios importantes** en un changelog

---

## ⚠️ Comandos Peligrosos (¡Ten cuidado!)

Estos comandos pueden eliminar datos:

```bash
# NO uses estos en producción sin backup
python manage.py flush          # Borra toda la DB
python manage.py migrate --fake # Puede causar inconsistencias
git push --force               # Puede sobrescribir historial
```

---

**Guarda este archivo como referencia rápida** 📌















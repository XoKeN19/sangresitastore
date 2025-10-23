# Instrucciones de Despliegue a Render

## ✅ Archivos de Configuración Creados

Ya he creado todos los archivos necesarios para el despliegue:

- ✅ `requirements.txt` - Dependencias de Python
- ✅ `build.sh` - Script de construcción para Render
- ✅ `.gitignore` - Archivos a excluir del repositorio
- ✅ `runtime.txt` - Versión de Python
- ✅ `cowork/settings.py` - Actualizado para producción
- ✅ `env.example` - Plantilla de variables de entorno

## 📋 Pasos a Seguir

### 1. Instalar Git (si no lo tienes)

Descarga e instala Git desde: https://git-scm.com/download/win

Después de instalar, reinicia tu terminal o IDE.

### 2. Inicializar Repositorio Git

Abre una terminal en el directorio de tu proyecto y ejecuta:

```bash
git init
git add .
git commit -m "Initial commit - Proyecto Django para Render"
```

### 3. Crear Repositorio en GitHub

1. Ve a https://github.com y crea una cuenta (si no tienes una)
2. Haz clic en "New repository" (botón verde)
3. Nombre del repositorio: `cowork-django` (o el que prefieras)
4. **NO** marques "Initialize with README"
5. Haz clic en "Create repository"

### 4. Conectar y Subir tu Código a GitHub

GitHub te mostrará comandos. Usa estos (reemplaza con tu URL):

```bash
git remote add origin https://github.com/TU-USUARIO/cowork-django.git
git branch -M main
git push -u origin main
```

Si te pide credenciales, usa tu usuario de GitHub y un **Personal Access Token** (no tu contraseña):
- Crear token: GitHub → Settings → Developer settings → Personal access tokens → Generate new token
- Permisos necesarios: `repo`

### 5. Crear Cuenta en Render

1. Ve a https://render.com
2. Haz clic en "Get Started for Free"
3. Regístrate con tu cuenta de GitHub (recomendado)
4. Autoriza a Render para acceder a tu cuenta de GitHub

### 6. Crear Base de Datos PostgreSQL en Render

1. En el dashboard de Render, haz clic en "New +"
2. Selecciona "PostgreSQL"
3. Configuración:
   - **Name**: `cowork-db` (o el nombre que prefieras)
   - **Database**: `cowork_db`
   - **User**: (déjalo como está)
   - **Region**: Oregon (o el más cercano)
   - **PostgreSQL Version**: 16
   - **Plan**: Free
4. Haz clic en "Create Database"
5. **IMPORTANTE**: Guarda la "Internal Database URL" (la necesitarás después)

### 7. Crear Web Service en Render

1. En el dashboard de Render, haz clic en "New +"
2. Selecciona "Web Service"
3. Conecta tu repositorio de GitHub
4. Configuración:
   - **Name**: `cowork-app` (o el nombre que prefieras)
   - **Region**: Oregon (la misma que la base de datos)
   - **Branch**: `main`
   - **Root Directory**: (déjalo vacío)
   - **Runtime**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn cowork.wsgi:application`
   - **Plan**: Free

### 8. Configurar Variables de Entorno en Render

En la sección "Environment Variables" del Web Service, agrega:

**Variable 1:**
- **Key**: `SECRET_KEY`
- **Value**: (genera una nueva clave secreta - ver abajo)

**Variable 2:**
- **Key**: `DEBUG`
- **Value**: `False`

**Variable 3:**
- **Key**: `ALLOWED_HOSTS`
- **Value**: `.onrender.com`

**Variable 4:**
- **Key**: `DATABASE_URL`
- **Value**: (copia la "Internal Database URL" de tu base de datos PostgreSQL)

**Variable 5:**
- **Key**: `PYTHON_VERSION`
- **Value**: `3.11.7`

#### Generar SECRET_KEY

Ejecuta esto en Python para generar una nueva SECRET_KEY:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

O en línea de comandos:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 9. Desplegar

1. Haz clic en "Create Web Service"
2. Render comenzará a construir y desplegar tu aplicación
3. Esto tomará varios minutos la primera vez
4. Verás los logs en tiempo real

### 10. Crear Superusuario

Una vez que el despliegue sea exitoso:

1. En Render, ve a tu Web Service
2. Haz clic en "Shell" en el menú izquierdo
3. Ejecuta:
   ```bash
   python manage.py createsuperuser
   ```
4. Sigue las instrucciones para crear tu usuario admin

### 11. Acceder a tu Aplicación

Tu aplicación estará disponible en:
`https://cowork-app.onrender.com` (reemplaza con tu nombre de servicio)

Para acceder al panel de administración:
`https://cowork-app.onrender.com/admin`

## ⚠️ Consideraciones Importantes

### Archivos Media

Los archivos en la carpeta `media/` (imágenes subidas) **NO** se incluirán en el repositorio Git.

**Opciones:**

1. **Subir manualmente**: Usa la shell de Render para subir archivos
2. **Usar almacenamiento externo** (recomendado para producción):
   - Cloudinary (gratis hasta 25GB)
   - AWS S3
   - Configurar con Django Storages

### Plan Gratuito de Render

- El servicio se "duerme" después de 15 minutos de inactividad
- Primera carga después de dormir puede tardar 30-60 segundos
- 750 horas gratis al mes
- Base de datos expira después de 90 días (puedes crear una nueva)

### Base de Datos

Tu base de datos SQLite local **NO** se transferirá a producción. Necesitarás:
- Recrear datos en producción, o
- Exportar datos de SQLite e importar a PostgreSQL

## 🔄 Actualizaciones Futuras

Cuando hagas cambios en tu código:

```bash
git add .
git commit -m "Descripción de los cambios"
git push
```

Render detectará automáticamente los cambios y redesplegará tu aplicación.

## 🆘 Solución de Problemas

### Error en Build

Si el build falla, revisa:
1. Los logs en Render
2. Que todas las variables de entorno estén configuradas
3. Que `build.sh` tenga permisos de ejecución (Git en Windows puede causar problemas)

### Error de Static Files

Si los archivos estáticos no cargan:
1. Verifica que `STATIC_ROOT` esté configurado
2. Asegúrate de que `collectstatic` se ejecutó (está en `build.sh`)
3. Revisa que WhiteNoise esté en MIDDLEWARE

### Error de Base de Datos

Si hay errores de conexión a la base de datos:
1. Verifica que `DATABASE_URL` esté correctamente configurada
2. Asegúrate de que la base de datos y el web service estén en la misma región
3. Usa la "Internal Database URL", no la "External"

## 📚 Recursos Adicionales

- Documentación de Render: https://render.com/docs
- Django Deployment Checklist: https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/
- Django on Render: https://render.com/docs/deploy-django

## ✅ Checklist Final

Antes de desplegar, verifica:

- [ ] Git instalado
- [ ] Repositorio creado en GitHub
- [ ] Código subido a GitHub
- [ ] Cuenta en Render creada
- [ ] Base de datos PostgreSQL creada en Render
- [ ] Variables de entorno configuradas
- [ ] Web Service creado
- [ ] Despliegue exitoso
- [ ] Superusuario creado
- [ ] Aplicación accesible en la URL de Render

---

**¡Buena suerte con tu despliegue!** Si tienes problemas, revisa los logs en Render o consulta la documentación.


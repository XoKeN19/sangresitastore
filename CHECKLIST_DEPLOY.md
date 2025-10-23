# ✅ Checklist de Despliegue a Render

Usa este checklist para asegurarte de completar todos los pasos necesarios.

---

## 📦 Preparación Local

### Instalaciones y Configuración
- [ ] Git instalado en tu computadora
- [ ] Cuenta de GitHub creada
- [ ] Cuenta de Render creada
- [ ] Archivos de configuración verificados:
  - [ ] requirements.txt existe
  - [ ] build.sh existe
  - [ ] .gitignore existe
  - [ ] runtime.txt existe
  - [ ] settings.py actualizado

---

## 🔧 Git y GitHub

### Inicializar Git Local
- [ ] Abrí terminal en la carpeta del proyecto
- [ ] Ejecuté `git init`
- [ ] Ejecuté `git add .`
- [ ] Ejecuté `git commit -m "Initial commit - Proyecto Django para Render"`
- [ ] No hubo errores en el commit

### Crear Repositorio en GitHub
- [ ] Fui a https://github.com/new
- [ ] Creé un nuevo repositorio
- [ ] NO marqué "Initialize with README"
- [ ] Copié la URL del repositorio

### Conectar y Subir
- [ ] Ejecuté `git remote add origin [URL]`
- [ ] Ejecuté `git branch -M main`
- [ ] Ejecuté `git push -u origin main`
- [ ] El código se subió exitosamente
- [ ] Puedo ver mi código en GitHub

---

## 🗄️ Base de Datos en Render

### Crear PostgreSQL
- [ ] Entré a mi dashboard de Render
- [ ] Click en "New +" → "PostgreSQL"
- [ ] Configuré el nombre: `cowork-db`
- [ ] Seleccioné región: Oregon
- [ ] Seleccioné plan: Free
- [ ] Click en "Create Database"
- [ ] La base de datos se creó exitosamente
- [ ] Copié la "Internal Database URL"
- [ ] Guardé la URL en un lugar seguro

---

## 🌐 Web Service en Render

### Crear Web Service
- [ ] Click en "New +" → "Web Service"
- [ ] Conecté mi cuenta de GitHub
- [ ] Seleccioné el repositorio correcto
- [ ] Configuré:
  - [ ] Name: `cowork-app` (o el que elegí)
  - [ ] Region: Oregon (misma que la DB)
  - [ ] Branch: `main`
  - [ ] Runtime: Python 3
  - [ ] Build Command: `./build.sh`
  - [ ] Start Command: `gunicorn cowork.wsgi:application`
  - [ ] Plan: Free

### Variables de Entorno
- [ ] Generé una nueva SECRET_KEY
- [ ] Agregué variable: `SECRET_KEY` = [mi clave generada]
- [ ] Agregué variable: `DEBUG` = `False`
- [ ] Agregué variable: `ALLOWED_HOSTS` = `.onrender.com`
- [ ] Agregué variable: `DATABASE_URL` = [mi Internal DB URL]
- [ ] Agregué variable: `PYTHON_VERSION` = `3.11.7`
- [ ] Guardé todas las variables

### Desplegar
- [ ] Click en "Create Web Service"
- [ ] El build empezó automáticamente
- [ ] Esperé a que termine el build (5-10 minutos)
- [ ] El deploy fue exitoso (status: "Live")
- [ ] No hay errores en los logs

---

## 👤 Configuración Post-Deploy

### Crear Superusuario
- [ ] En Render, fui a mi Web Service
- [ ] Click en "Shell" en el menú
- [ ] Ejecuté: `python manage.py createsuperuser`
- [ ] Ingresé username, email y password
- [ ] El superusuario se creó exitosamente

### Verificar Aplicación
- [ ] Abrí la URL de mi app: `https://[mi-app].onrender.com`
- [ ] La página de inicio carga correctamente
- [ ] Los archivos estáticos (CSS) se ven bien
- [ ] Probé el login
- [ ] Accedí al admin: `https://[mi-app].onrender.com/admin`
- [ ] Pude loguearme con el superusuario

---

## 📁 Archivos Media (Opcional)

### Si necesitas subir imágenes/archivos
- [ ] Decidí qué hacer con los archivos media:
  - [ ] Los subiré manualmente via Shell de Render
  - [ ] Configuraré almacenamiento externo (Cloudinary/S3)
  - [ ] Los recrearé en producción

---

## 🧪 Pruebas Funcionales

### Verificar Funcionalidades
- [ ] Registro de usuarios funciona
- [ ] Login funciona
- [ ] Carrito de compras funciona
- [ ] Ver videojuegos funciona
- [ ] Ver coleccionables funciona
- [ ] Pedidos funcionan
- [ ] Panel de admin accesible
- [ ] Todas las páginas cargan sin errores

---

## 📝 Documentación

### Guardar Información Importante
- [ ] Guardé la URL de mi aplicación
- [ ] Guardé las credenciales del superusuario
- [ ] Guardé la URL del repositorio GitHub
- [ ] Documenté cualquier configuración especial

---

## 🔄 Actualizaciones Futuras

### Proceso para Actualizar
Cuando hagas cambios:
- [ ] Hago cambios en el código local
- [ ] `git add .`
- [ ] `git commit -m "Descripción del cambio"`
- [ ] `git push`
- [ ] Render detecta y redespliega automáticamente
- [ ] Verifico que los cambios se aplicaron

---

## 🎉 ¡Completado!

Si marcaste todas las casillas, ¡tu aplicación está desplegada exitosamente!

**URL de mi aplicación:** `https://_________________.onrender.com`

**Próximos pasos:**
- Compartir la URL con otros
- Considerar un dominio personalizado
- Configurar almacenamiento de archivos media
- Monitorear el uso y logs
- Planear migraciones de datos si es necesario

---

## 🆘 ¿Problemas?

Si algo no funcionó, revisa:
1. **DEPLOY_INSTRUCTIONS.md** - Instrucciones detalladas
2. **RENDER_ENV_VARS.md** - Configuración de variables
3. **Logs en Render** - Errores específicos
4. **Documentación de Render** - https://render.com/docs

---

## 📊 Monitoreo

Cosas a revistar regularmente:
- [ ] Revisar logs de errores en Render
- [ ] Verificar que la app está "Live"
- [ ] Monitorear uso de la base de datos
- [ ] Backup de datos importantes (la DB gratis expira en 90 días)

---

**Última actualización:** {{ Fecha de tu deploy }}


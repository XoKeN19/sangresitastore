# ✅ Checklist de Despliegue a Railway

Usa este checklist para asegurarte de completar todos los pasos necesarios.

---

## 📦 Preparación Local

### Instalaciones y Configuración
- [ ] Git instalado en tu computadora
- [ ] Cuenta de GitHub creada
- [ ] Cuenta de Railway creada
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
- [ ] Ejecuté `git commit -m "Initial commit - Proyecto Django para Railway"`
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

## 🚂 Proyecto en Railway

### Crear Proyecto
- [ ] Entré a mi dashboard de Railway
- [ ] Click en "New Project"
- [ ] Seleccioné "Deploy from GitHub repo"
- [ ] Elegí mi repositorio `cowork-django`
- [ ] Railway detectó Django automáticamente

### Agregar PostgreSQL
- [ ] En mi proyecto, click en "New"
- [ ] Seleccioné "Database" → "Add PostgreSQL"
- [ ] La base de datos se creó automáticamente
- [ ] Railway conectó DATABASE_URL automáticamente

### Variables de Entorno
- [ ] Generé una nueva SECRET_KEY
- [ ] Agregué variable: `SECRET_KEY` = [mi clave generada]
- [ ] Agregué variable: `DEBUG` = `False`
- [ ] Agregué variable: `ALLOWED_HOSTS` = `.railway.app`
- [ ] Agregué variable: `PYTHON_VERSION` = `3.11.7`
- [ ] Guardé todas las variables

### Desplegar
- [ ] Railway desplegó automáticamente
- [ ] Esperé a que termine el build (3-5 minutos)
- [ ] El deploy fue exitoso (status: "Active")
- [ ] No hay errores en los logs

### Generar Dominio
- [ ] Fui a Settings → Domains
- [ ] Click en "Generate Domain"
- [ ] Obtuve mi URL: `https://mi-app.railway.app`

---

## 👤 Configuración Post-Deploy

### Crear Superusuario
- [ ] En Railway, fui a mi Web Service
- [ ] Click en "..." (tres puntos) → "Terminal"
- [ ] Ejecuté: `python manage.py createsuperuser`
- [ ] Ingresé username, email y password
- [ ] El superusuario se creó exitosamente

### Verificar Aplicación
- [ ] Abrí la URL de mi app: `https://mi-app.railway.app`
- [ ] La página de inicio carga correctamente
- [ ] Los archivos estáticos (CSS) se ven bien
- [ ] Probé el login
- [ ] Accedí al admin: `https://mi-app.railway.app/admin`
- [ ] Pude loguearme con el superusuario

---

## 📁 Archivos Media (Opcional)

### Si necesitas subir imágenes/archivos
- [ ] Decidí qué hacer con los archivos media:
  - [ ] Los subiré manualmente via Terminal de Railway
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
1. **RAILWAY_DEPLOY.md** - Instrucciones detalladas
2. **RAILWAY_RAPIDO.md** - Guía rápida
3. **Logs en Railway** - Errores específicos
4. **Documentación de Railway** - https://docs.railway.app

---

## 📊 Monitoreo

Cosas a revisar regularmente:
- [ ] Revisar logs de errores en Railway
- [ ] Verificar que la app está "Active"
- [ ] Monitorear uso del crédito (Dashboard → Usage)
- [ ] Backup de datos importantes

---

**Última actualización:** {{ Fecha de tu deploy }}


# 🚂 Deploy a Railway - Guía Completa

Railway es más simple que Render y detecta Django automáticamente.

---

## ⚡ Inicio Rápido (5 pasos)

### 1. Git y GitHub (5 min)
```bash
git init
git add .
git commit -m "Initial commit"
```

Luego en GitHub (https://github.com/new):
- Crea repositorio: `cowork-django`
- NO marques README
- Crea y copia la URL

```bash
git remote add origin https://github.com/TU-USUARIO/cowork-django.git
git branch -M main
git push -u origin main
```

### 2. Crear Cuenta en Railway (1 min)
1. Ve a https://railway.app
2. Click "Login" → "Login with GitHub"
3. Autoriza Railway

### 3. Crear Nuevo Proyecto (2 min)
1. Dashboard de Railway → "New Project"
2. Selecciona "Deploy from GitHub repo"
3. Selecciona tu repositorio `cowork-django`
4. Railway detectará Django automáticamente

### 4. Agregar PostgreSQL (1 min)
1. En tu proyecto, click "New" → "Database" → "Add PostgreSQL"
2. ¡Listo! Railway conecta automáticamente

### 5. Variables de Entorno (2 min)
En tu servicio web, ve a "Variables" y agrega:

```
SECRET_KEY = [genera nueva - ver abajo]
DEBUG = False
ALLOWED_HOSTS = .railway.app
```

**Generar SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Deploy
Railway despliega automáticamente. Espera 3-5 minutos.

---

## 📋 Guía Paso a Paso Detallada

### Paso 1: Preparar el Código

Ya tienes todo listo, solo necesitas subirlo a GitHub.

**1.1 Verificar archivos:**
```bash
python verificar_proyecto.py
```

**1.2 Inicializar Git:**
```bash
git init
```

**1.3 Agregar archivos:**
```bash
git add .
```

**1.4 Commit inicial:**
```bash
git commit -m "Initial commit - Django para Railway"
```

---

### Paso 2: Subir a GitHub

**2.1 Crear repositorio:**
- Ve a https://github.com/new
- Nombre: `cowork-django` (o el que prefieras)
- Descripción: "Tienda de videojuegos Django"
- **NO** marques "Initialize with README"
- Click "Create repository"

**2.2 Conectar y subir:**
```bash
git remote add origin https://github.com/TU-USUARIO/cowork-django.git
git branch -M main
git push -u origin main
```

Si pide credenciales:
- Usuario: tu username de GitHub
- Password: Personal Access Token (https://github.com/settings/tokens)

---

### Paso 3: Crear Cuenta en Railway

**3.1 Registrarse:**
1. Ve a https://railway.app
2. Click en "Login"
3. Selecciona "Login with GitHub"
4. Autoriza Railway para acceder a tu GitHub

**3.2 Verificar cuenta:**
- Railway te da $5 de crédito gratis al mes
- Puedes usar plan gratuito o conectar tarjeta para más recursos

---

### Paso 4: Crear Proyecto en Railway

**4.1 Nuevo Proyecto:**
1. En el dashboard, click "New Project"
2. Selecciona "Deploy from GitHub repo"
3. Busca y selecciona tu repositorio `cowork-django`
4. Railway comenzará a analizar el repo

**4.2 Configuración Automática:**
Railway detectará:
- ✅ Que es un proyecto Python
- ✅ El archivo `requirements.txt`
- ✅ Que es Django
- ✅ El comando de inicio apropiado

---

### Paso 5: Agregar Base de Datos PostgreSQL

**5.1 Agregar PostgreSQL:**
1. En tu proyecto, click en el botón "New"
2. Selecciona "Database"
3. Click en "Add PostgreSQL"
4. Railway creará la base de datos automáticamente

**5.2 Conexión Automática:**
Railway automáticamente:
- Crea una variable `DATABASE_URL`
- La conecta con tu aplicación
- ¡No necesitas copiar/pegar nada!

---

### Paso 6: Configurar Variables de Entorno

**6.1 Ir a Variables:**
1. Click en tu servicio web (el que tiene tu código)
2. Ve a la pestaña "Variables"
3. Click en "New Variable"

**6.2 Agregar Variables:**

**Variable 1 - SECRET_KEY:**
```
Key: SECRET_KEY
Value: [genera una nueva - ver comando abajo]
```

Generar:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Variable 2 - DEBUG:**
```
Key: DEBUG
Value: False
```

**Variable 3 - ALLOWED_HOSTS:**
```
Key: ALLOWED_HOSTS
Value: .railway.app
```

**Variable 4 - PYTHON_VERSION:**
```
Key: PYTHON_VERSION
Value: 3.11.7
```

**6.3 Guardar:**
Click "Add" para cada variable.

---

### Paso 7: Configurar Build y Start

Railway debería detectar esto automáticamente, pero por si acaso:

**7.1 Ir a Settings:**
1. Click en tu servicio web
2. Ve a "Settings"

**7.2 Verificar comandos:**
- **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate`
- **Start Command:** `gunicorn cowork.wsgi:application --bind 0.0.0.0:$PORT`

Si no están configurados, agrégalos.

---

### Paso 8: Deploy

**8.1 Deploy Automático:**
Railway desplegará automáticamente. Verás:
- 🔵 Building...
- 🟡 Deploying...
- 🟢 Active (cuando termine)

**8.2 Ver Logs:**
Click en "Deployments" para ver los logs en tiempo real.

**8.3 Esperar:**
El primer deploy toma 3-5 minutos.

---

### Paso 9: Obtener URL Pública

**9.1 Generar Dominio:**
1. En tu servicio web, ve a "Settings"
2. Busca la sección "Domains"
3. Click "Generate Domain"
4. Railway te dará una URL: `https://tu-app.railway.app`

**9.2 Actualizar ALLOWED_HOSTS (si es necesario):**
Si tu dominio es específico, actualiza la variable:
```
ALLOWED_HOSTS = tu-app.railway.app,.railway.app
```

---

### Paso 10: Crear Superusuario

**10.1 Abrir Terminal:**
1. En tu servicio web, busca el botón "..." (tres puntos)
2. Selecciona "Terminal" o "Shell"
3. Espera a que cargue

**10.2 Crear Superusuario:**
```bash
python manage.py createsuperuser
```

Sigue las instrucciones:
- Username: [tu usuario]
- Email: [tu email]
- Password: [tu contraseña]
- Confirmar password

**10.3 Verificar:**
Ve a `https://tu-app.railway.app/admin` y loguéate.

---

## ✅ Verificación Final

### Probar la Aplicación

1. **Página Principal:**
   ```
   https://tu-app.railway.app
   ```

2. **Panel Admin:**
   ```
   https://tu-app.railway.app/admin
   ```

3. **Verificar que funcione:**
   - [ ] La página carga correctamente
   - [ ] Los estilos CSS se ven bien
   - [ ] Puedes hacer login
   - [ ] El admin funciona
   - [ ] Puedes crear/editar contenido

---

## 🔄 Actualizaciones Futuras

### Cada vez que hagas cambios:

```bash
git add .
git commit -m "Descripción del cambio"
git push
```

Railway redesplegará automáticamente. Toma 2-3 minutos.

---

## 🆘 Solución de Problemas

### Error: "Application failed to respond"
**Causa:** Gunicorn no está iniciando correctamente.

**Solución:**
1. Ve a Settings → Start Command
2. Verifica que sea: `gunicorn cowork.wsgi:application --bind 0.0.0.0:$PORT`

---

### Error: "Invalid HTTP_HOST header"
**Causa:** ALLOWED_HOSTS no incluye tu dominio.

**Solución:**
1. Ve a Variables
2. Actualiza ALLOWED_HOSTS: `.railway.app,tu-dominio.railway.app`
3. Redespliega

---

### Error: "No module named X"
**Causa:** Falta una dependencia en requirements.txt

**Solución:**
1. Agrega la dependencia a `requirements.txt`
2. `git add requirements.txt`
3. `git commit -m "Add dependency"`
4. `git push`

---

### Archivos estáticos no cargan
**Causa:** collectstatic no se ejecutó.

**Solución:**
1. Ve a Settings → Build Command
2. Asegúrate que incluya: `python manage.py collectstatic --no-input`
3. Fuerza un redeploy

---

### Base de datos no conecta
**Causa:** DATABASE_URL no está configurada.

**Solución:**
1. Verifica que PostgreSQL esté agregado al proyecto
2. Railway debería crear `DATABASE_URL` automáticamente
3. Verifica en Variables que existe
4. Si no existe, Railway la creará cuando agregues PostgreSQL

---

## 💰 Planes y Límites

### Plan Gratuito ($5/mes de crédito)
- ✅ Suficiente para proyectos pequeños
- ✅ PostgreSQL incluido
- ✅ Deploy automático
- ✅ 500MB de RAM
- ⚠️ El servicio NO se duerme (ventaja vs Render)

### Uso Estimado
- Aplicación web simple: ~$3-4/mes
- Con PostgreSQL: incluido en el costo
- Si superas $5, necesitarás agregar tarjeta

### Monitorear Uso
1. Dashboard → "Usage"
2. Ve cuánto crédito llevas usado
3. Railway te avisa cuando te acercas al límite

---

## 📊 Comparación: Railway vs Render

| Característica | Railway | Render |
|----------------|---------|--------|
| Setup | 🟢 Más fácil | 🟡 Manual |
| PostgreSQL | 🟢 1 click | 🟢 1 click |
| Auto-detección | 🟢 Sí | 🟡 Parcial |
| Plan Gratis | $5 crédito | Sí, limitado |
| Sleep | 🟢 No | 🔴 Sí (15 min) |
| Interface | 🟢 Moderna | 🟢 Clara |
| Documentación | 🟢 Buena | 🟢 Excelente |

---

## 🎯 Ventajas de Railway

1. **Detección Automática:** Reconoce Django y configura todo
2. **No se Duerme:** Tu app siempre está disponible
3. **PostgreSQL Fácil:** Se conecta automáticamente
4. **Interface Simple:** Más intuitiva que Render
5. **Deploy Rápido:** 2-3 minutos vs 5-10 en Render
6. **Terminal Incluido:** Para crear superusuario fácilmente

---

## 📚 Recursos

- **Dashboard:** https://railway.app/dashboard
- **Documentación:** https://docs.railway.app
- **Discord:** https://discord.gg/railway
- **Status:** https://status.railway.app

---

## 🎓 Tips

1. **Usa el Terminal de Railway** para comandos de Django
2. **Revisa los logs** si algo falla
3. **Monitorea el uso** para no exceder el crédito gratuito
4. **Haz commits descriptivos** para identificar cambios
5. **Prueba localmente** antes de hacer push

---

## 🔐 Seguridad

- ✅ Genera una nueva SECRET_KEY (no uses la de desarrollo)
- ✅ Mantén DEBUG=False en producción
- ✅ No subas archivos .env a GitHub
- ✅ Usa HTTPS (Railway lo proporciona gratis)
- ✅ Cambia contraseñas de admin regularmente

---

## ⚡ Comandos Útiles (Railway Terminal)

### Migrations
```bash
python manage.py migrate
python manage.py makemigrations
python manage.py showmigrations
```

### Superusuario
```bash
python manage.py createsuperuser
```

### Shell
```bash
python manage.py shell
```

### Ver Logs
```bash
# En Railway, ve a "Deployments" y selecciona el deployment actual
```

---

## ✨ Conclusión

Railway es más simple que Render porque:
- Detecta Django automáticamente
- PostgreSQL se conecta solo
- No necesitas configurar tanto manualmente
- La interfaz es más intuitiva

**¡Tu app estará en línea en menos de 15 minutos!**

---

**Siguiente:** Después del deploy, lee `COMANDOS_UTILES.md` para mantenimiento.











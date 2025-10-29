# ⚡ Railway Deploy - Inicio Súper Rápido

## Pre-requisitos (10 min para instalar)
- [ ] Git instalado: https://git-scm.com/download/win
- [ ] Cuenta GitHub: https://github.com (gratis)
- [ ] Cuenta Railway: https://railway.app (login con GitHub)

---

## 💾 ¿Tienes Datos en SQLite?

Si quieres mantener tus datos actuales, lee primero:
```
📖 MIGRAR_RAPIDO.md (5 min)
```

Si no tienes datos o quieres empezar de cero, continúa abajo ⬇️

---

## 5 Pasos al Deploy

### 1️⃣ Git Local (3 min)
```bash
git init
git add .
git commit -m "Initial commit"
```

### 2️⃣ GitHub (3 min)
1. https://github.com/new
2. Nombre: `cowork-django`
3. NO marcar README
4. Crear

```bash
git remote add origin https://github.com/TU-USUARIO/cowork-django.git
git branch -M main
git push -u origin main
```

### 3️⃣ Railway Proyecto (2 min)
1. https://railway.app → Login with GitHub
2. New Project → Deploy from GitHub
3. Selecciona tu repo

### 4️⃣ PostgreSQL (30 seg)
En tu proyecto Railway:
1. New → Database → PostgreSQL
2. ¡Listo! (se conecta solo)

### 5️⃣ Variables (2 min)
Click en tu web service → Variables → Add:

```
SECRET_KEY = [corre: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"]
DEBUG = False
ALLOWED_HOSTS = .railway.app
PYTHON_VERSION = 3.11.7
```

---

## 🎉 Deploy Automático

Railway despliega solo. Espera 3-5 min.

---

## 🌐 Obtener URL

Settings → Domains → Generate Domain

Tu app: `https://tu-app.railway.app`

---

## 👤 Crear Admin

Railway → Tu servicio → ⋮ (tres puntos) → Terminal

```bash
python manage.py createsuperuser
```

Admin: `https://tu-app.railway.app/admin`

---

## 🔄 Actualizar

```bash
git add .
git commit -m "cambios"
git push
```

Railway redespliega automáticamente (2-3 min).

---

## 📖 Más Detalles

Lee: **RAILWAY_DEPLOY.md** para guía completa.

---

## 🆘 Problemas?

**No inicia:**
- Settings → Start Command: `gunicorn cowork.wsgi:application --bind 0.0.0.0:$PORT`

**Error HTTP_HOST:**
- Variables → ALLOWED_HOSTS: `.railway.app`

**Revisar Logs:**
- Deployments → Click en el último

---

## 💡 Ventajas de Railway

✅ Detecta Django automáticamente  
✅ PostgreSQL se conecta solo  
✅ No se duerme (vs Render)  
✅ Deploy en 3 minutos  
✅ $5 gratis/mes  

---

**Total: 15 minutos del inicio al deploy** ⚡




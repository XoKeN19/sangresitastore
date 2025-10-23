# ⚡ Inicio Rápido - Deploy en 10 Minutos

Si tienes prisa, sigue estos pasos. Para detalles, ve a DEPLOY_INSTRUCTIONS.md

## Pre-requisitos
- [ ] Git instalado: https://git-scm.com/download/win
- [ ] Cuenta GitHub: https://github.com
- [ ] Cuenta Render: https://render.com

---

## Paso 1: Git (2 min)

```bash
git init
git add .
git commit -m "Initial commit"
```

---

## Paso 2: GitHub (2 min)

1. Ve a https://github.com/new
2. Nombre: `cowork-django`
3. NO marques README
4. Crea el repo
5. Ejecuta:

```bash
git remote add origin https://github.com/TU-USUARIO/cowork-django.git
git branch -M main
git push -u origin main
```

---

## Paso 3: Render - Base de Datos (1 min)

1. https://render.com → New + → PostgreSQL
2. Name: `cowork-db`
3. Plan: Free
4. Create Database
5. **Copia "Internal Database URL"**

---

## Paso 4: Render - Web Service (3 min)

1. New + → Web Service
2. Conecta tu repo de GitHub
3. Configuración:
   - Build: `./build.sh`
   - Start: `gunicorn cowork.wsgi:application`
   - Plan: Free

---

## Paso 5: Variables de Entorno (2 min)

En "Environment Variables", agrega:

```
SECRET_KEY = [genera con: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"]
DEBUG = False
ALLOWED_HOSTS = .onrender.com
DATABASE_URL = [pega la Internal Database URL del paso 3]
PYTHON_VERSION = 3.11.7
```

---

## Paso 6: Deploy (5-10 min)

1. Click "Create Web Service"
2. Espera a que termine el build
3. Cuando esté "Live", ve a Shell
4. Ejecuta: `python manage.py createsuperuser`
5. ¡Listo!

---

## Tu App

URL: `https://TU-APP.onrender.com`
Admin: `https://TU-APP.onrender.com/admin`

---

## ¿Problemas?

Lee: **DEPLOY_INSTRUCTIONS.md**

---

## Actualizar después

```bash
git add .
git commit -m "Cambios"
git push
```

Render redespliega automáticamente.


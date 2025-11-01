# 🔄 Migrar Datos de SQLite a PostgreSQL

Guía para migrar tus datos locales de SQLite a PostgreSQL en Railway sin hacerlo manualmente.

---

## 📋 Proceso General

```
SQLite Local → Exportar JSON → Desplegar Railway → Importar JSON → PostgreSQL
```

**Tiempo total:** 5-10 minutos

---

## Paso 1: Exportar Datos de SQLite Local (2 min)

### 1.1 Verificar que tu servidor local funcione

```bash
python manage.py runserver
```

Si funciona, ciérralo (Ctrl+C).

### 1.2 Exportar TODOS los datos

```bash
python manage.py dumpdata > datos_backup.json
```

Esto crea un archivo `datos_backup.json` con todos tus datos.

### 1.3 Exportar solo datos importantes (Recomendado)

Si el archivo es muy grande o quieres solo ciertos datos:

```bash
# Solo datos de tu app (sin auth/sessions)
python manage.py dumpdata eva_3 > datos_eva3.json

# O datos específicos:
python manage.py dumpdata eva_3.Videojuego > videojuegos.json
python manage.py dumpdata eva_3.Coleccionable > coleccionables.json
python manage.py dumpdata eva_3.Usuario > usuarios.json
```

**Recomendación:** Usa `datos_eva3.json` (solo tu app).

---

## Paso 2: Subir el Archivo a Git (1 min)

### 2.1 Agregar a .gitignore TEMPORALMENTE

Primero, verifica que `datos_eva3.json` NO esté en `.gitignore`. Si está, sácalo temporalmente.

### 2.2 Subir a GitHub

```bash
git add datos_eva3.json
git commit -m "Add database backup for migration"
git push
```

**Nota:** Después del deploy, puedes eliminar este archivo del repo si quieres.

---

## Paso 3: Desplegar a Railway (10 min)

Sigue la guía normal de Railway:

1. Crea proyecto en Railway
2. Conecta tu repo de GitHub
3. **Agrega PostgreSQL** (este es el paso importante)
4. Configura variables de entorno
5. Espera a que despliegue

**Railway creará una base de datos PostgreSQL vacía.**

---

## Paso 4: Importar Datos en Railway (3 min)

### 4.1 Abrir Terminal de Railway

1. En Railway, ve a tu Web Service
2. Click en "..." (tres puntos)
3. Selecciona "Terminal" o "Shell"
4. Espera a que cargue

### 4.2 Verificar que el archivo esté ahí

```bash
ls -la
```

Deberías ver `datos_eva3.json` en la lista.

### 4.3 Importar los datos

```bash
python manage.py loaddata datos_eva3.json
```

Si usaste otro nombre:
```bash
python manage.py loaddata datos_backup.json
```

**¡Listo!** Tus datos ahora están en PostgreSQL.

---

## Paso 5: Crear Superusuario (Si no se migró)

Si tu usuario admin no funcionó o quieres crear uno nuevo:

```bash
python manage.py createsuperuser
```

---

## 🎯 Comando Rápido (Todo en Uno)

Si quieres exportar todo lo importante en un solo comando:

```bash
# Local - Exportar
python manage.py dumpdata --exclude auth.permission --exclude contenttypes --exclude admin.logentry --exclude sessions.session > datos_limpios.json

# Subir
git add datos_limpios.json
git commit -m "Database backup"
git push

# Railway Terminal - Importar (después del deploy)
python manage.py loaddata datos_limpios.json
```

---

## ⚠️ Solución de Problemas

### Error: "Could not load contenttypes.ContentType"

**Solución:** Excluye contenttypes al exportar:

```bash
python manage.py dumpdata --exclude contenttypes > datos.json
```

### Error: "Duplicate key violation"

**Causa:** Intentas importar datos que ya existen.

**Solución:** Limpia la base de datos primero (Railway Terminal):

```bash
python manage.py flush --no-input
python manage.py loaddata datos_eva3.json
```

### Error: "No such file 'datos_eva3.json'"

**Causa:** El archivo no se subió a GitHub.

**Solución:**
1. Verifica que el archivo esté en tu repo local
2. Asegúrate de hacer `git add` y `git push`
3. Espera a que Railway redespliega

### Los usuarios no pueden hacer login

**Causa:** Las contraseñas están hasheadas diferente.

**Solución:** 
- Opción 1: Usa el superusuario y cambia contraseñas desde admin
- Opción 2: Crea nuevos usuarios

---

## 📝 Script Automatizado (Opcional)

Puedes crear un script para automatizar el proceso:

**Archivo: `exportar_datos.py`**

```python
#!/usr/bin/env python
import os
import subprocess
import sys

print("🔄 Exportando datos de SQLite...")

# Exportar datos
result = subprocess.run([
    sys.executable, 
    'manage.py', 
    'dumpdata',
    '--exclude', 'auth.permission',
    '--exclude', 'contenttypes',
    '--exclude', 'admin.logentry',
    '--exclude', 'sessions.session',
    '--natural-foreign',
    '--natural-primary',
    '--indent', '2'
], capture_output=True, text=True)

if result.returncode == 0:
    with open('datos_migration.json', 'w', encoding='utf-8') as f:
        f.write(result.stdout)
    print("✅ Datos exportados a: datos_migration.json")
    print(f"📊 Tamaño: {len(result.stdout)} caracteres")
else:
    print("❌ Error al exportar:")
    print(result.stderr)
    sys.exit(1)
```

**Uso:**
```bash
python exportar_datos.py
```

---

## 🎓 Explicación de los Comandos

### dumpdata
Exporta datos de la base de datos a formato JSON.

```bash
python manage.py dumpdata [app_name] [options] > archivo.json
```

**Opciones útiles:**
- `--exclude`: Excluir ciertos modelos
- `--natural-foreign`: Usa valores naturales en lugar de IDs
- `--indent 2`: Formato legible (bonito)

### loaddata
Importa datos desde un archivo JSON a la base de datos.

```bash
python manage.py loaddata archivo.json
```

Django automáticamente:
- Detecta el tipo de base de datos
- Convierte los datos al formato correcto
- Maneja las relaciones entre tablas

---

## 💡 Consejos

### 1. Haz Backup Regularmente

Crea un backup antes de hacer cambios grandes:

```bash
python manage.py dumpdata eva_3 > backup_$(date +%Y%m%d).json
```

### 2. No Subas Datos Sensibles

Si tienes datos sensibles, NO los subas a GitHub:

1. Agrega `*.json` a `.gitignore`
2. Usa otro método (SCP, Railway CLI, etc.)

### 3. Prueba Localmente Primero

Antes de subir a producción, prueba el proceso localmente:

```bash
# Crear DB temporal
python manage.py migrate --database=default

# Cargar datos
python manage.py loaddata datos_eva3.json

# Verificar
python manage.py runserver
```

### 4. Limpia Datos Viejos

Después de una migración exitosa, puedes:

```bash
# Eliminar del repo
git rm datos_eva3.json
git commit -m "Remove database backup after migration"
git push
```

---

## 🔄 Workflow Completo

```bash
# === PASO 1: LOCAL ===
# Exportar datos
python manage.py dumpdata eva_3 --indent 2 > datos_eva3.json

# Verificar que se exportó
cat datos_eva3.json  # Linux/Mac
type datos_eva3.json  # Windows

# === PASO 2: GIT ===
git add datos_eva3.json
git commit -m "Add database for migration"
git push

# === PASO 3: RAILWAY ===
# (Hacer deploy normal siguiendo RAILWAY_RAPIDO.md)

# === PASO 4: RAILWAY TERMINAL ===
# Abrir terminal en Railway y ejecutar:
python manage.py loaddata datos_eva3.json

# Verificar
python manage.py shell
>>> from eva_3.models import Videojuego
>>> print(Videojuego.objects.count())
>>> exit()

# === PASO 5: LIMPIAR (Opcional) ===
# Local:
git rm datos_eva3.json
git commit -m "Clean up migration file"
git push
```

---

## 📊 Verificación Post-Migración

Después de importar, verifica que todo esté bien:

### En Railway Terminal:

```bash
# Ver cantidad de registros
python manage.py shell
>>> from eva_3.models import *
>>> print(f"Videojuegos: {Videojuego.objects.count()}")
>>> print(f"Coleccionables: {Coleccionable.objects.count()}")
>>> print(f"Usuarios: {Usuario.objects.count()}")
>>> exit()
```

### En el Admin:

1. Ve a `https://tu-app.railway.app/admin`
2. Login con tu superusuario
3. Verifica que veas todos tus datos

---

## 🆘 Si Algo Sale Mal

### Empezar de Nuevo

Si algo salió mal y quieres reiniciar:

```bash
# Railway Terminal
python manage.py flush --no-input
python manage.py migrate
python manage.py loaddata datos_eva3.json
python manage.py createsuperuser
```

### Backup de Emergencia

Si perdiste datos, puedes:

1. Reconectar a tu SQLite local
2. Exportar de nuevo
3. Reimportar a Railway

---

## ✅ Checklist de Migración

- [ ] Servidor local funciona con SQLite
- [ ] Exporté datos: `python manage.py dumpdata eva_3 > datos_eva3.json`
- [ ] Verifiqué que el archivo existe y tiene contenido
- [ ] Subí a Git: `git add datos_eva3.json && git commit && git push`
- [ ] Desplegué a Railway con PostgreSQL
- [ ] Abrí Terminal en Railway
- [ ] Importé datos: `python manage.py loaddata datos_eva3.json`
- [ ] Verifiqué que los datos estén ahí
- [ ] Creé superusuario si es necesario
- [ ] Probé el admin y la app
- [ ] (Opcional) Limpié el archivo del repo

---

## 🎉 ¡Migración Completa!

Después de seguir estos pasos:

✅ Tus datos de SQLite están en PostgreSQL  
✅ No tuviste que recrear nada manualmente  
✅ Todos los modelos, relaciones y datos se mantienen  
✅ Tu app funciona igual que en local  

---

**Siguiente:** Continúa con el deploy siguiendo `RAILWAY_RAPIDO.md`

**Problemas?** Lee la sección "Solución de Problemas" arriba










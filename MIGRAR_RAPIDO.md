# ⚡ Migrar Datos - Versión Rápida

Migra tus datos de SQLite a PostgreSQL en 5 minutos.

---

## 🎯 3 Comandos Esenciales

### 1️⃣ En tu Computadora (Local)

Exporta tus datos:

```bash
python manage.py dumpdata eva_3 > datos.json
```

Sube a GitHub:

```bash
git add datos.json
git commit -m "Database backup"
git push
```

### 2️⃣ Despliega a Railway

Sigue `RAILWAY_RAPIDO.md` normalmente:
- Conecta GitHub
- Agrega PostgreSQL ← **IMPORTANTE**
- Configura variables
- Espera a que despliegue

### 3️⃣ En Railway Terminal

Importa tus datos:

```bash
python manage.py loaddata datos.json
```

**¡Listo!** Tus datos están en PostgreSQL 🎉

---

## 🔍 Verificar que Funcionó

En Railway Terminal:

```bash
python manage.py shell
>>> from eva_3.models import Videojuego, Coleccionable
>>> print(Videojuego.objects.count())
>>> print(Coleccionable.objects.count())
>>> exit()
```

---

## 🆘 Si Hay Error

### Error: "Could not load contenttypes"

Usa este comando en LOCAL:

```bash
python manage.py dumpdata --exclude contenttypes --exclude auth.permission > datos.json
```

Luego sube y carga de nuevo.

### Error: "File not found"

El archivo no se subió a GitHub:

```bash
# Verifica que esté
git status

# Si no está, agrégalo
git add datos.json
git commit -m "Add data"
git push
```

### Empezar de Nuevo

En Railway Terminal:

```bash
python manage.py flush --no-input
python manage.py loaddata datos.json
```

---

## 📋 Checklist

- [ ] Exporté: `python manage.py dumpdata eva_3 > datos.json`
- [ ] Subí: `git add datos.json && git push`
- [ ] Desplegué a Railway con PostgreSQL
- [ ] Importé: `python manage.py loaddata datos.json`
- [ ] Verifiqué que los datos estén ahí

---

## ⏰ Timeline

```
Exportar datos: 30 seg
Subir a Git: 30 seg
Deploy Railway: 3-5 min (automático)
Importar datos: 30 seg

Total: ~5 minutos
```

---

**Versión Detallada:** Lee `MIGRAR_DATOS.md` para más información

**Deploy:** Continúa con `RAILWAY_RAPIDO.md`








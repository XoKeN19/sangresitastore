# 📋 ORDEN DE PASOS - Seguir en Este Orden

Lee y sigue estos archivos EN ESTE ORDEN exacto.

---

## 🎯 CASO A: Tienes Datos en SQLite que Quieres Mantener

### PASO 1: Instalar Git
```
https://git-scm.com/download/win
```
Descarga, instala, reinicia terminal.

Verifica: `git --version`

---

### PASO 2: Exportar Datos
📖 **Abre y sigue:** `MIGRAR_RAPIDO.md`

**Resumen:**
```bash
python manage.py dumpdata eva_3 > datos.json
git add datos.json
git commit -m "Database backup"
git push
```

---

### PASO 3: Deploy a Railway
📖 **Abre y sigue:** `RAILWAY_RAPIDO.md`

**Resumen:**
- Subir código a GitHub
- Crear proyecto en Railway
- Agregar PostgreSQL
- Configurar variables
- Esperar deploy

---

### PASO 4: Importar Datos
**En Railway Terminal:**
```bash
python manage.py loaddata datos.json
```

---

### PASO 5: Crear Superusuario
**En Railway Terminal:**
```bash
python manage.py createsuperuser
```

---

### PASO 6: Verificar
Ve a: `https://tu-app.railway.app/admin`

✅ **¡LISTO!**

---

## 🎯 CASO B: NO Tienes Datos (Empiezas de Cero)

### PASO 1: Instalar Git
```
https://git-scm.com/download/win
```
Descarga, instala, reinicia terminal.

Verifica: `git --version`

---

### PASO 2: Deploy a Railway
📖 **Abre y sigue:** `RAILWAY_RAPIDO.md`

**Resumen:**
- Git init, add, commit
- Subir a GitHub
- Crear proyecto en Railway
- Agregar PostgreSQL
- Configurar variables
- Esperar deploy

---

### PASO 3: Crear Superusuario
**En Railway Terminal:**
```bash
python manage.py createsuperuser
```

---

### PASO 4: Agregar Contenido
Ve a: `https://tu-app.railway.app/admin`

Agrega tus videojuegos, coleccionables, etc.

✅ **¡LISTO!**

---

## 📚 Archivos de Referencia (DESPUÉS del Deploy)

Estos los lees DESPUÉS si los necesitas:

- **COMANDOS_UTILES.md** - Comandos para actualizar, mantener, etc.
- **CHECKLIST_DEPLOY.md** - Para verificar que no te saltaste nada
- **RAILWAY_DEPLOY.md** - Guía detallada si tienes problemas

---

## ⏰ Tiempo Estimado

### Con Datos (Caso A):
```
Git instalado: 10 min
Exportar datos: 2 min
Deploy Railway: 15 min
Importar datos: 2 min
Total: ~30 min
```

### Sin Datos (Caso B):
```
Git instalado: 10 min
Deploy Railway: 15 min
Total: ~25 min
```

---

## 🆘 Si Tienes Problemas

1. **Git no funciona:** Reinicia la terminal después de instalar
2. **Error al exportar:** Lee `MIGRAR_DATOS.md`
3. **Error en Railway:** Lee `RAILWAY_DEPLOY.md` → Solución de Problemas
4. **Otra cosa:** Lee `INDICE_DOCUMENTACION.md` para buscar ayuda

---

## ✅ Checklist Rápido

**Caso A (Con Datos):**
- [ ] Git instalado
- [ ] Datos exportados (`datos.json`)
- [ ] Código en GitHub
- [ ] Proyecto en Railway
- [ ] PostgreSQL agregado
- [ ] Variables configuradas
- [ ] Deploy completado
- [ ] Datos importados
- [ ] Superusuario creado
- [ ] App funciona

**Caso B (Sin Datos):**
- [ ] Git instalado
- [ ] Código en GitHub
- [ ] Proyecto en Railway
- [ ] PostgreSQL agregado
- [ ] Variables configuradas
- [ ] Deploy completado
- [ ] Superusuario creado
- [ ] App funciona

---

## 🎯 Resumen Ultra Simple

```
┌─────────────────────────────────────┐
│ ¿TIENES DATOS QUE MANTENER?         │
└─────────────┬───────────────────────┘
              │
      ┌───────┴────────┐
      │                │
     SÍ               NO
      │                │
      ▼                ▼
1. MIGRAR_RAPIDO   1. RAILWAY_RAPIDO
2. RAILWAY_RAPIDO  2. Crear superusuario
3. Importar datos  3. ¡Listo!
4. ¡Listo!
```

---

## 📖 ¿Qué Dice Cada Archivo?

### MIGRAR_RAPIDO.md
- Cómo exportar tus datos de SQLite
- 3 comandos simples
- 5 minutos

### RAILWAY_RAPIDO.md
- Cómo subir a GitHub
- Cómo crear proyecto en Railway
- Cómo configurar variables
- 15 minutos

### COMANDOS_UTILES.md
- Comandos para después del deploy
- Actualizar, mantener, debug
- Referencia

---

## 👉 EMPIEZA AQUÍ AHORA:

**¿Tienes datos en SQLite local?**

**SÍ →** Abre: `MIGRAR_RAPIDO.md`

**NO →** Abre: `RAILWAY_RAPIDO.md`

---

**¡Sigue el orden y estarás en internet en 25-30 minutos!** 🚀










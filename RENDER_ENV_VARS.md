# Variables de Entorno para Render

Estas son las variables de entorno que debes configurar en Render cuando crees tu Web Service.

## Variables Requeridas

### 1. SECRET_KEY
```
Nombre: SECRET_KEY
Valor: [Genera una nueva clave secreta]
```

**Cómo generar:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Ejemplo de valor:**
```
django-insecure-a8f&2k9*mz$4p6@xn2v!q7w8e5r4t6y9u0i8o7p6a5s4d3f2g1h
```

---

### 2. DEBUG
```
Nombre: DEBUG
Valor: False
```

**IMPORTANTE:** Siempre debe ser `False` en producción.

---

### 3. ALLOWED_HOSTS
```
Nombre: ALLOWED_HOSTS
Valor: .onrender.com
```

Esto permitirá que tu app funcione en cualquier subdominio de Render.

Si quieres usar un dominio personalizado, agrégalo separado por comas:
```
.onrender.com,tudominio.com,www.tudominio.com
```

---

### 4. DATABASE_URL
```
Nombre: DATABASE_URL
Valor: [Copiado desde tu Base de Datos PostgreSQL en Render]
```

**Cómo obtenerlo:**
1. En Render, ve a tu base de datos PostgreSQL
2. Busca "Internal Database URL"
3. Copia el valor completo (empieza con `postgresql://`)

**Formato:**
```
postgresql://usuario:password@host:5432/nombre_db
```

**IMPORTANTE:** Usa la URL **Internal**, no la External.

---

### 5. PYTHON_VERSION
```
Nombre: PYTHON_VERSION
Valor: 3.11.7
```

---

## Resumen Rápido

Copia y pega estos nombres y valores en Render:

| Variable Name    | Value                                    |
|------------------|------------------------------------------|
| SECRET_KEY       | [genera una nueva - ver arriba]         |
| DEBUG            | False                                    |
| ALLOWED_HOSTS    | .onrender.com                            |
| DATABASE_URL     | [copia desde tu DB PostgreSQL]           |
| PYTHON_VERSION   | 3.11.7                                   |

---

## Configuración en Render

### Paso a Paso:

1. Ve a tu Web Service en Render
2. Click en "Environment" en el menú izquierdo
3. En "Environment Variables", click "Add Environment Variable"
4. Para cada variable:
   - Ingresa el **Key** (nombre)
   - Ingresa el **Value** (valor)
   - Click "Save"
5. Después de agregar todas, Render redesplegará automáticamente

---

## Variables Opcionales

Estas son opcionales pero útiles:

### WEB_CONCURRENCY
```
Nombre: WEB_CONCURRENCY
Valor: 4
```
Número de workers de Gunicorn. En el plan gratuito, 2-4 es suficiente.

---

## Verificación

Después de configurar las variables, verifica en los logs que:

1. La aplicación inicia correctamente
2. No hay errores de variables de entorno faltantes
3. La conexión a la base de datos funciona
4. Los archivos estáticos se sirven correctamente

---

## Solución de Problemas

### Error: "KeyError: 'SECRET_KEY'"
- Verifica que agregaste la variable SECRET_KEY
- Asegúrate de que no tiene espacios al inicio o final

### Error: "Invalid HTTP_HOST header"
- Verifica que ALLOWED_HOSTS incluya `.onrender.com`
- O agrega el dominio específico de tu app

### Error: "could not connect to server"
- Verifica que DATABASE_URL esté correctamente configurada
- Asegúrate de usar la URL Internal de la base de datos
- Confirma que la base de datos está en la misma región que el web service

---

## Seguridad

⚠️ **IMPORTANTE:**
- NUNCA compartas tu SECRET_KEY públicamente
- NUNCA subas archivos .env al repositorio
- NUNCA uses DEBUG=True en producción
- La DATABASE_URL contiene credenciales sensibles - manténla privada


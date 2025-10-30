# Comandos Git para Deploy

## Instalación de Git

Si Git no está instalado, descárgalo desde:
https://git-scm.com/download/win

## Pasos Rápidos

### 1. Inicializar Git (solo la primera vez)
```bash
git init
```

### 2. Agregar todos los archivos
```bash
git add .
```

### 3. Hacer commit inicial
```bash
git commit -m "Initial commit - Proyecto Django para Render"
```

### 4. Crear repositorio en GitHub
1. Ve a https://github.com/new
2. Nombre: `cowork-django`
3. NO marques "Initialize with README"
4. Click en "Create repository"

### 5. Conectar con GitHub (reemplaza TU-USUARIO con tu usuario de GitHub)
```bash
git remote add origin https://github.com/TU-USUARIO/cowork-django.git
git branch -M main
git push -u origin main
```

## Para futuras actualizaciones

```bash
git add .
git commit -m "Descripción de los cambios"
git push
```

## Verificar estado
```bash
git status
```

## Ver historial
```bash
git log --oneline
```

## Nota sobre Credenciales

Si GitHub te pide contraseña, necesitas usar un **Personal Access Token**:

1. Ve a https://github.com/settings/tokens
2. Click en "Generate new token (classic)"
3. Dale un nombre descriptivo
4. Marca el checkbox "repo"
5. Click en "Generate token"
6. **GUARDA EL TOKEN** - solo lo verás una vez
7. Usa este token como "contraseña" cuando Git te lo pida











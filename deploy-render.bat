@echo off
echo ========================================
echo Script de Deploy para Render
echo ========================================
echo.

echo Verificando si Git esta instalado...
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git no esta instalado
    echo.
    echo Por favor descarga e instala Git desde:
    echo https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo [OK] Git esta instalado
echo.

echo ========================================
echo PASO 1: Inicializar repositorio Git
echo ========================================
if exist .git (
    echo [INFO] Repositorio Git ya inicializado
) else (
    git init
    echo [OK] Repositorio Git inicializado
)
echo.

echo ========================================
echo PASO 2: Agregar archivos
echo ========================================
git add .
echo [OK] Archivos agregados
echo.

echo ========================================
echo PASO 3: Crear commit
echo ========================================
git commit -m "Initial commit - Proyecto Django para Render"
if errorlevel 1 (
    echo [INFO] No hay cambios para commitear o ya se hizo commit
) else (
    echo [OK] Commit creado
)
echo.

echo ========================================
echo PASO 4: Conectar con GitHub
echo ========================================
echo.
echo Ahora necesitas:
echo 1. Crear un repositorio en GitHub: https://github.com/new
echo 2. Copiar la URL del repositorio (ejemplo: https://github.com/usuario/repo.git)
echo.
set /p REPO_URL="Pega la URL de tu repositorio de GitHub: "

if "%REPO_URL%"=="" (
    echo [ERROR] No proporcionaste una URL
    pause
    exit /b 1
)

git remote remove origin >nul 2>&1
git remote add origin %REPO_URL%
git branch -M main
echo [OK] Repositorio remoto configurado
echo.

echo ========================================
echo PASO 5: Subir codigo a GitHub
echo ========================================
echo.
echo Se te pediran tus credenciales de GitHub:
echo - Usuario: tu nombre de usuario de GitHub
echo - Password: usa un Personal Access Token (NO tu contraseña)
echo.
echo Si no tienes un token, crealo en:
echo https://github.com/settings/tokens
echo (Marca el checkbox 'repo')
echo.
pause

git push -u origin main
if errorlevel 1 (
    echo [ERROR] No se pudo subir el codigo
    echo Verifica tus credenciales y la URL del repositorio
    pause
    exit /b 1
)

echo.
echo ========================================
echo [EXITO] Codigo subido a GitHub
echo ========================================
echo.
echo Siguientes pasos:
echo 1. Ve a https://render.com y crea una cuenta
echo 2. Conecta tu cuenta de GitHub
echo 3. Crea una base de datos PostgreSQL
echo 4. Crea un Web Service conectado a tu repositorio
echo.
echo Consulta DEPLOY_INSTRUCTIONS.md para instrucciones detalladas
echo.
pause


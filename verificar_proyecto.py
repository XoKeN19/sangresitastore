#!/usr/bin/env python
"""
Script de verificación pre-deploy
Ejecuta esto antes de subir a Render para verificar la configuración
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, required=True):
    """Verifica si un archivo existe"""
    exists = Path(filepath).exists()
    symbol = "✅" if exists else ("❌" if required else "⚠️")
    status = "OK" if exists else ("FALTA" if required else "Opcional")
    print(f"{symbol} {filepath}: {status}")
    return exists

def check_settings():
    """Verifica configuración de settings.py"""
    print("\n📝 Verificando settings.py...")
    
    try:
        # Verificar imports
        with open('cowork/settings.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        checks = {
            'import dj_database_url': 'Importa dj_database_url',
            'from decouple import': 'Importa decouple',
            'whitenoise': 'WhiteNoise configurado',
            'STATIC_ROOT': 'STATIC_ROOT definido',
            'DATABASE_URL': 'Configuración de PostgreSQL',
        }
        
        for check, description in checks.items():
            if check in content:
                print(f"  ✅ {description}")
            else:
                print(f"  ❌ {description}")
                
    except FileNotFoundError:
        print("  ❌ No se encuentra settings.py")
        return False
    
    return True

def main():
    print("=" * 60)
    print("🔍 VERIFICACIÓN PRE-DEPLOY PARA RENDER")
    print("=" * 60)
    
    print("\n📦 Verificando archivos esenciales...")
    
    files_required = [
        'requirements.txt',
        'build.sh',
        '.gitignore',
        'runtime.txt',
        'manage.py',
        'cowork/settings.py',
        'cowork/wsgi.py',
    ]
    
    files_optional = [
        'render.yaml',
        'README.md',
        'DEPLOY_INSTRUCTIONS.md',
    ]
    
    all_good = True
    
    for file in files_required:
        if not check_file_exists(file, required=True):
            all_good = False
    
    for file in files_optional:
        check_file_exists(file, required=False)
    
    # Verificar settings.py
    if not check_settings():
        all_good = False
    
    # Verificar estructura de directorios
    print("\n📁 Verificando estructura de directorios...")
    
    dirs = ['static', 'eva_3', 'eva_3/templates']
    for dir_path in dirs:
        exists = Path(dir_path).exists()
        symbol = "✅" if exists else "❌"
        print(f"{symbol} {dir_path}/")
        if not exists:
            all_good = False
    
    # Recomendaciones
    print("\n💡 Recomendaciones:")
    print("  1. Asegúrate de tener Git instalado")
    print("  2. Crea una cuenta en Render.com")
    print("  3. Crea una cuenta en GitHub")
    print("  4. Genera un nuevo SECRET_KEY para producción")
    print("  5. Lee DEPLOY_INSTRUCTIONS.md para el proceso completo")
    
    # Resultado final
    print("\n" + "=" * 60)
    if all_good:
        print("✅ ¡TODO LISTO! Tu proyecto está preparado para deploy")
        print("\nPróximos pasos:")
        print("  1. git init")
        print("  2. git add .")
        print("  3. git commit -m 'Initial commit'")
        print("  4. Crear repositorio en GitHub")
        print("  5. git push")
        print("  6. Configurar en Render")
    else:
        print("❌ HAY PROBLEMAS - Revisa los errores arriba")
        print("\nSoluciona los problemas marcados con ❌ antes de continuar")
    
    print("=" * 60)
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())












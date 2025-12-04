#!/usr/bin/env python3
"""
Script de ejemplo para probar la funcionalidad básica de AudioATexto
Este script verifica que las dependencias estén instaladas correctamente
"""

import sys

def check_dependencies():
    """Verifica que todas las dependencias estén instaladas"""
    print("Verificando dependencias...")
    print("-" * 50)
    
    dependencies = {
        'tkinter': 'tkinter (GUI)',
        'vosk': 'vosk',
        'soundfile': 'soundfile',
        'numpy': 'numpy',
        'noisereduce': 'noisereduce',
        'pydub': 'pydub',
        'scipy': 'scipy'
    }
    
    all_ok = True
    
    for module, name in dependencies.items():
        try:
            if module == 'tkinter':
                import tkinter
            else:
                __import__(module)
            print(f"✓ {name:<20} - OK")
        except ImportError as e:
            print(f"✗ {name:<20} - NO INSTALADO")
            all_ok = False
    
    print("-" * 50)
    
    if all_ok:
        print("\n✓ Todas las dependencias están instaladas correctamente")
        return True
    else:
        print("\n✗ Faltan dependencias. Por favor ejecuta:")
        print("   pip install -r requirements.txt")
        return False


def check_vosk_model():
    """Verifica si existe un modelo de Vosk"""
    import os
    
    print("\nVerificando modelo de Vosk...")
    print("-" * 50)
    
    model_paths = [
        "model",
        "vosk-model-es",
        "vosk-model-small-es"
    ]
    
    found = False
    for path in model_paths:
        if os.path.exists(path):
            print(f"✓ Modelo encontrado en: {path}")
            found = True
            break
    
    if not found:
        print("✗ No se encontró el modelo de Vosk")
        print("\nPara descargar un modelo:")
        print("1. Visita: https://alphacephei.com/vosk/models")
        print("2. Descarga 'vosk-model-small-es-0.42' o 'vosk-model-es-0.42'")
        print("3. Extrae el archivo y renombra la carpeta a 'model'")
        print("4. Coloca la carpeta 'model' en el directorio de la aplicación")
    
    print("-" * 50)
    return found


def main():
    """Función principal"""
    print("=" * 50)
    print("AudioATexto - Verificación del Sistema")
    print("=" * 50)
    print()
    
    # Verificar dependencias
    deps_ok = check_dependencies()
    
    # Verificar modelo
    model_ok = check_vosk_model()
    
    print("\nResumen:")
    print("=" * 50)
    
    if deps_ok and model_ok:
        print("✓ El sistema está listo para usar")
        print("\nPara iniciar la aplicación, ejecuta:")
        print("   python main.py")
    elif deps_ok:
        print("⚠ Dependencias OK, pero falta el modelo de Vosk")
        print("  Descarga el modelo para usar la aplicación")
    else:
        print("✗ Faltan dependencias necesarias")
        print("  Instala las dependencias antes de continuar")
    
    print("=" * 50)


if __name__ == "__main__":
    main()

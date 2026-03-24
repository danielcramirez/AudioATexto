# AudioATexto

Aplicación de transcripción de audio a texto en español usando Vosk. Soporta archivos WAV, OGG, MP3 y M4A, con funciones de mejora de audio, reducción de ruido, verificación de calidad y diarización de voces.

Tambien permite generar un resumen estructurado de una reunion usando Google Gemini API.

## Inicio Rápido (clonando repositorio en Windows)

Si clonaste este proyecto, ejecuta un solo comando para dejar todo listo:

```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```

Tambien puedes hacerlo con doble clic en:

```text
setup.bat
```

Este script hace automaticamente:

- Instalar Python 3.12 (si no existe)
- Crear entorno virtual `.venv312`
- Instalar dependencias de `requirements.txt`
- Descargar modelo Vosk en español en `model/`
- Descargar FFmpeg portable en `ffmpeg/`

Luego ejecuta la app con:

```powershell
.\.venv312\Scripts\python.exe .\Audio.py
```

O desde VS Code:

- `Ctrl+Shift+B` (tarea `Ejecutar AudioATexto`)

## 🚀 Descarga Rápida (Windows)

**¿Solo quieres usar la aplicación?** Descarga el ejecutable listo para usar:

📥 **[Descargar AudioATexto.exe](dist/AudioATexto.exe)** (Incluye todas las dependencias)

> ⚠️ **Nota**: El ejecutable es grande (~varios GB) porque incluye el modelo de reconocimiento de voz completo.

### Uso del ejecutable:
1. Descarga `AudioATexto.exe`
2. Haz doble clic para ejecutar
3. ¡Listo! No necesitas instalar Python ni dependencias

## Características

- 🎙️ **Transcripción de audio** a texto en español usando el modelo Vosk
- 🔊 **Soporte para múltiples formatos**: WAV, OGG, MP3 y M4A
- 🎚️ **Mejora de audio**: Reducción de ruido automática
- 📊 **Verificación de calidad**: Análisis de nivel de señal
- 👥 **Diarización de voces**: Identificación de diferentes hablantes
- 💾 **Exportación automática**: Guarda la transcripción en archivos .txt
- 📝 **Resumen de reunión con IA**: Genera resumen ejecutivo, decisiones y próximos pasos con Google Gemini
- 📄 **Acta automática en LaTeX**: Genera un archivo `.tex` diligenciado con estructura de acta de reunión
- 📑 **Acta automática en PDF**: Compila el `.tex` a PDF desde la aplicación (si `pdflatex` está instalado)
- 🗂️ **Acta automática en Word**: Genera también `.docx` en el mismo flujo de exportación
- 🖥️ **Interfaz gráfica**: Fácil de usar con Tkinter

## Requisitos (solo para desarrollo)

- Python 3.12 recomendado
- Modelo Vosk en español en `model/`
- FFmpeg (si usas MP3/M4A)

## Instalación manual (para desarrolladores)

1. Clona este repositorio:
```bash
git clone https://github.com/danielcramirez/AudioATexto.git
cd AudioATexto
```

2. Crea y activa un entorno virtual (recomendado 3.12):
```bash
py -3.12 -m venv .venv312
.\.venv312\Scripts\activate  # En Windows
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Descarga el modelo Vosk en español:
   - Descarga desde: https://alphacephei.com/vosk/models
   - Extrae el modelo en la carpeta `model/`

5. Instala FFmpeg (solo necesario para MP3/M4A):
   - Opcion recomendada: usar `setup.ps1` para dejarlo local en `ffmpeg/`
   - Si lo instalas manualmente en el sistema, verifica que `ffmpeg` y `ffprobe` esten en el `PATH`

## Uso

### Opción 1: Ejecutable (Recomendado para usuarios)
```bash
.\dist\AudioATexto.exe
```

### Opción 2: Desde código fuente
```bash
python Audio.py
```

### Funciones disponibles:

1. **Seleccionar Audio**: Elige un archivo WAV, OGG, MP3 o M4A
2. **Verificar Calidad**: Analiza la calidad del audio
3. **Mejorar Audio**: Elimina ruido de fondo
4. **Identificar Voces**: Detecta diferentes hablantes
5. **Transcribir Audio**: Convierte el audio a texto y guarda en .txt
6. **Resumir Reunion (Google AI)**: Genera un resumen de la transcripción y lo guarda en `_resumen_reunion.txt`
7. **Generar Acta LaTeX**: Crea un archivo de acta con la información detectada en la transcripción
8. **Generar Acta PDF + Word**: Genera el `.tex`, el `.docx` y compila a `.pdf` en un solo paso

Si Google API responde error 429 por cuota agotada, la app genera automaticamente un resumen local de respaldo y lo guarda en `_resumen_reunion_local.txt`.

## Resumen de reunión con Google Gemini

Para usar el resumen con IA necesitas una API key de Google AI Studio.

Opciones para configurar la API key:

1. En la interfaz, en el campo **Google API Key (Gemini)**.
2. Como variable de entorno `GEMINI_API_KEY`.

Flujo recomendado:

1. Selecciona un audio.
2. Haz clic en **Transcribir Audio**.
3. Haz clic en **Resumir Reunion (Google AI)**.

Archivos generados:

- `*_transcripcion.txt`
- `*_resumen_reunion.txt`
- `*_resumen_reunion_local.txt` (cuando no hay cuota en Google API)
- `*_acta_reunion.tex`
- `*_acta_reunion_local.tex` (cuando no hay cuota en Google API)
- `*_acta_reunion.pdf`
- `*_acta_reunion_local.pdf` (cuando no hay cuota en Google API)
- `*_acta_reunion.docx`
- `*_acta_reunion_local.docx` (cuando no hay cuota en Google API)

## Generacion de Acta en LaTeX

Flujo sugerido:

1. Selecciona un audio.
2. Ejecuta **Transcribir Audio**.
3. (Opcional) Ingresa API key para mejor calidad de llenado.
4. Ejecuta **Generar Acta LaTeX**.

Si quieres PDF y Word directamente, usa **Generar Acta PDF + Word**.

La app intentara llenar automaticamente la estructura del acta con la transcripcion.
Si Google API no tiene cuota, la app generara una version local de respaldo.

Para generar PDF desde la app necesitas un compilador LaTeX en PATH (`pdflatex`), por ejemplo MiKTeX o TeX Live.

## 🔧 Crear el ejecutable

Si quieres generar tu propio ejecutable:

```bash
# Instalar PyInstaller
pip install pyinstaller

# Generar el ejecutable
pyinstaller AudioATexto.spec --clean
```

El ejecutable se generará en `dist/AudioATexto.exe`

### Detalles técnicos del ejecutable:
- Incluye todas las dependencias de Python
- Incluye DLLs nativas de Vosk
- Incluye el modelo de reconocimiento completo
- Detecta automáticamente si se ejecuta desde `.exe` o Python
- No requiere instalación, es portable

## Licencia

Este proyecto está licenciado bajo GNU General Public License v3.0 - ver el archivo LICENSE para más detalles.

## Autor

Daniel Ramírez - [@danielcramirez](https://github.com/danielcramirez)

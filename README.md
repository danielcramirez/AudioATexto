# AudioATexto

Aplicación de transcripción de audio a texto en español usando Vosk. Soporta archivos WAV y OGG, con funciones de mejora de audio, reducción de ruido, verificación de calidad y diarización de voces.

## Características

- 🎙️ **Transcripción de audio** a texto en español usando el modelo Vosk
- 🔊 **Soporte para múltiples formatos**: WAV y OGG
- 🎚️ **Mejora de audio**: Reducción de ruido automática
- 📊 **Verificación de calidad**: Análisis de nivel de señal
- 👥 **Diarización de voces**: Identificación de diferentes hablantes
- 💾 **Exportación automática**: Guarda la transcripción en archivos .txt
- 🖥️ **Interfaz gráfica**: Fácil de usar con Tkinter

## Requisitos

- Python 3.8 o superior
- Modelo Vosk en español (debe estar en la carpeta `model/`)

## Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/danielcramirez/AudioATexto.git
cd AudioATexto
```

2. Crea y activa un entorno virtual:
```bash
python -m venv venv
.\venv\Scripts\activate  # En Windows
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Descarga el modelo Vosk en español:
   - Descarga desde: https://alphacephei.com/vosk/models
   - Extrae el modelo en la carpeta `model/`

## Uso

Ejecuta la aplicación:
```bash
python Audio.py
```

### Funciones disponibles:

1. **Seleccionar Audio**: Elige un archivo WAV u OGG
2. **Verificar Calidad**: Analiza la calidad del audio
3. **Mejorar Audio**: Elimina ruido de fondo
4. **Identificar Voces**: Detecta diferentes hablantes
5. **Transcribir Audio**: Convierte el audio a texto y guarda en .txt

## Licencia

Este proyecto está licenciado bajo GNU General Public License v3.0 - ver el archivo LICENSE para más detalles.

## Autor

Daniel Ramírez - [@danielcramirez](https://github.com/danielcramirez)

# AudioATexto

Aplicación GUI de transcripción de audio a texto en español usando Vosk. Soporta archivos WAV y OGG, con funciones de mejora de audio, reducción de ruido y exportación a texto.

## Características

- 🎙️ **Transcripción de audio a texto** usando el modelo Vosk para español
- 🎵 **Soporte para múltiples formatos**: WAV y OGG
- 🔊 **Mejora de audio**: Reducción de ruido y filtros pasa-banda
- 💾 **Exportación a texto**: Guarda las transcripciones en archivos TXT
- 🖥️ **Interfaz gráfica intuitiva** con Tkinter
- 📊 **Barra de progreso** para seguimiento de transcripción en tiempo real

## Requisitos

- Python 3.7 o superior
- Modelo de Vosk para español

## Instalación

1. **Clonar el repositorio**:
```bash
git clone https://github.com/danielcramirez/AudioATexto.git
cd AudioATexto
```

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Descargar el modelo de Vosk**:
   - Visita [https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models)
   - Descarga uno de los modelos en español:
     - `vosk-model-small-es-0.42` (ligero, ~39 MB)
     - `vosk-model-es-0.42` (completo, ~1.4 GB, mayor precisión)
   - Extrae el archivo descargado
   - Renombra la carpeta a `model` y colócala en el directorio de la aplicación

## Uso

1. **Ejecutar la aplicación**:
```bash
python main.py
```

2. **Transcribir audio**:
   - Haz clic en "Seleccionar Audio" para elegir un archivo WAV o OGG
   - Selecciona las opciones de procesamiento deseadas:
     - ✅ Reducción de ruido (recomendado)
     - ✅ Mejora de audio con filtro pasa-banda (recomendado)
   - Haz clic en "Iniciar Transcripción"
   - Espera a que se complete el proceso (verás el progreso en la barra)
   - El texto transcrito aparecerá en el área de resultados

3. **Exportar transcripción**:
   - Una vez completada la transcripción, haz clic en "Exportar a TXT"
   - Selecciona la ubicación y nombre del archivo
   - El texto se guardará en formato UTF-8

## Opciones de Procesamiento

### Reducción de Ruido
Elimina el ruido de fondo del audio usando algoritmos avanzados de procesamiento de señales, mejorando la claridad de la voz.

### Mejora de Audio
Aplica un filtro pasa-banda (300 Hz - 3400 Hz) que optimiza las frecuencias de la voz humana, mejorando la precisión de la transcripción.

## Estructura del Proyecto

```
AudioATexto/
├── main.py              # Aplicación principal con GUI
├── requirements.txt     # Dependencias del proyecto
├── README.md           # Este archivo
├── model/              # Carpeta para el modelo de Vosk (crear)
└── LICENSE             # Licencia del proyecto
```

## Dependencias

- **vosk**: Motor de reconocimiento de voz
- **pydub**: Manipulación de archivos de audio
- **numpy**: Procesamiento numérico
- **scipy**: Filtros de señales
- **noisereduce**: Reducción de ruido
- **soundfile**: Lectura/escritura de archivos de audio

## Solución de Problemas

### Error: "No se encontró el modelo de Vosk"
- Asegúrate de haber descargado y extraído el modelo de Vosk
- La carpeta del modelo debe estar en el directorio de la aplicación y llamarse `model`

### Error al importar dependencias
- Verifica que todas las dependencias estén instaladas: `pip install -r requirements.txt`

### No se detecta texto en el audio
- Verifica que el audio contenga voz en español
- Asegúrate de que el audio tenga buena calidad
- Prueba con las opciones de mejora de audio activadas

### Audio muy largo tarda mucho en procesar
- El procesamiento es en tiempo real, un audio de 5 minutos tarda aproximadamente 2-3 minutos
- Para mejores resultados, considera usar el modelo pequeño (vosk-model-small-es)

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request para sugerencias o mejoras.

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## Autor

Daniel Ramirez

## Reconocimientos

- [Vosk](https://alphacephei.com/vosk/) - Motor de reconocimiento de voz
- [Pydub](https://github.com/jiaaro/pydub) - Procesamiento de audio
- [Noisereduce](https://github.com/timsainb/noisereduce) - Reducción de ruido

# AudioATexto - Resumen del Proyecto

## 📋 Descripción General

AudioATexto es una aplicación de escritorio con interfaz gráfica (GUI) desarrollada en Python usando Tkinter, diseñada para transcribir audio a texto utilizando el motor de reconocimiento de voz Vosk. La aplicación está optimizada para audio en español y ofrece funcionalidades avanzadas de procesamiento de audio.

## 🎯 Características Principales

### Funcionalidades Core
- ✅ **Transcripción de audio a texto** usando Vosk
- ✅ **Soporte multi-formato**: WAV y OGG
- ✅ **Reducción de ruido** avanzada
- ✅ **Mejora de audio** con filtros pasa-banda (300-3400 Hz)
- ✅ **Exportación a TXT** con codificación UTF-8
- ✅ **Interfaz gráfica intuitiva** con Tkinter
- ✅ **Procesamiento en tiempo real** con barra de progreso
- ✅ **Threading** para interfaz no bloqueante

### Características Técnicas
- 🔧 **Cross-platform**: Windows, macOS, Linux
- 🔒 **Procesamiento local**: Sin envío de datos a internet
- 🧵 **Multi-threading**: UI responsiva durante procesamiento
- 📊 **Feedback visual**: Barra de progreso y mensajes de estado
- 🛡️ **Manejo robusto de errores**
- 🔄 **Conversión automática**: OGG → WAV cuando sea necesario

## 📁 Estructura del Proyecto

```
AudioATexto/
├── main.py                     # Aplicación principal con GUI
├── check_system.py             # Script de verificación del sistema
├── test_audio_app.py           # Suite de pruebas unitarias
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Documentación principal
├── USAGE_GUIDE.md              # Guía detallada de uso
├── INTERFACE_DESCRIPTION.md    # Descripción de la interfaz
├── PROJECT_SUMMARY.md          # Este archivo
├── LICENSE                     # Licencia MIT
├── .gitignore                  # Archivos excluidos del repo
└── model/                      # Directorio para modelo Vosk (no incluido)
```

## 🔧 Tecnologías Utilizadas

### Lenguaje
- **Python 3.7+**: Lenguaje principal

### Bibliotecas Principales
- **vosk (0.3.45)**: Motor de reconocimiento de voz
- **tkinter**: Framework de interfaz gráfica (incluido en Python)
- **pydub (0.25.1)**: Manipulación de archivos de audio
- **numpy (1.24.3)**: Operaciones numéricas y arrays
- **scipy (1.11.4)**: Procesamiento de señales y filtros
- **noisereduce (3.0.0)**: Reducción de ruido avanzada
- **soundfile (0.12.1)**: Lectura/escritura de audio

## 🏗️ Arquitectura

### Componentes Principales

#### 1. AudioTranscriptionApp (Clase Principal)
- **Responsabilidad**: Gestión de la interfaz y lógica de negocio
- **Métodos clave**:
  - `setup_ui()`: Configura la interfaz gráfica
  - `select_audio_file()`: Maneja la selección de archivos
  - `enhance_audio()`: Aplica mejoras al audio
  - `transcribe_audio()`: Realiza la transcripción
  - `export_to_text()`: Exporta el resultado

#### 2. Procesamiento de Audio
```python
Audio Input (WAV/OGG)
    ↓
Conversión a WAV (si es OGG)
    ↓
Carga con soundfile
    ↓
Conversión a mono (si es estéreo)
    ↓
Reducción de ruido (opcional)
    ↓
Filtro pasa-banda (opcional)
    ↓
Normalización
    ↓
Remuestreo a 16kHz
    ↓
Conversión a int16
    ↓
Vosk Recognizer
    ↓
Texto transcrito
```

#### 3. Threading Model
- **Thread Principal**: Interfaz gráfica (Tkinter)
- **Thread Secundario**: Procesamiento de audio (transcripción)
- **Comunicación**: Variables compartidas con sincronización

## 📊 Flujo de Datos

```
Usuario → Selección Archivo → Validación
                                    ↓
                            Opciones de Procesamiento
                                    ↓
                            Cargar Modelo Vosk
                                    ↓
                            Leer Audio
                                    ↓
                            Aplicar Mejoras
                                    ↓
                            Transcribir
                                    ↓
                            Mostrar Resultado
                                    ↓
Usuario ← Exportar TXT ← Texto Transcrito
```

## 🧪 Testing

### Suite de Pruebas (`test_audio_app.py`)
- ✅ Verificación de imports
- ✅ Validación de estructura de archivos
- ✅ Pruebas de lógica de procesamiento
- ✅ Validación de filtros de audio
- ✅ Pruebas de normalización

### Ejecución
```bash
python test_audio_app.py
```

## 🔒 Seguridad

### Análisis Realizados
- ✅ **CodeQL**: Sin vulnerabilidades detectadas
- ✅ **GitHub Advisory Database**: Todas las dependencias seguras
- ✅ **Validación de entrada**: Verificación de archivos
- ✅ **Manejo de excepciones**: Captura de todos los errores

### Mejores Prácticas Implementadas
- No se ejecuta código dinámico
- No hay conexiones de red
- Archivos temporales con `tempfile` (seguro)
- Validación de datos antes del procesamiento
- Clipping de audio para prevenir overflow

## 📈 Rendimiento

### Tiempos Aproximados
- **Modelo pequeño (vosk-model-small-es)**:
  - 1 min de audio ≈ 30-60 segundos de procesamiento
  - Uso de RAM: ~200-500 MB

- **Modelo completo (vosk-model-es)**:
  - 1 min de audio ≈ 60-90 segundos de procesamiento
  - Uso de RAM: ~1-2 GB

### Optimizaciones Implementadas
- Procesamiento por chunks (4000 samples)
- Threading para UI no bloqueante
- Reutilización del modelo Vosk
- Gestión eficiente de memoria

## 🚀 Instalación y Uso

### Instalación Rápida
```bash
# Clonar repositorio
git clone https://github.com/danielcramirez/AudioATexto.git
cd AudioATexto

# Instalar dependencias
pip install -r requirements.txt

# Descargar modelo Vosk (ejemplo con modelo pequeño)
wget https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip
unzip vosk-model-small-es-0.42.zip
mv vosk-model-small-es-0.42 model

# Verificar instalación
python check_system.py

# Ejecutar aplicación
python main.py
```

## 📚 Documentación Disponible

1. **README.md**: Documentación principal y guía de inicio
2. **USAGE_GUIDE.md**: Guía detallada de uso con ejemplos
3. **INTERFACE_DESCRIPTION.md**: Descripción completa de la interfaz
4. **PROJECT_SUMMARY.md**: Este archivo - resumen técnico

## 🔄 Mantenimiento

### Actualización de Dependencias
```bash
pip install -r requirements.txt --upgrade
```

### Verificación de Sistema
```bash
python check_system.py
```

### Pruebas
```bash
python test_audio_app.py
```

## 🤝 Contribuciones

El proyecto está abierto a contribuciones. Áreas de mejora potencial:
- Soporte para más idiomas
- Procesamiento batch de múltiples archivos
- Exportación a más formatos (PDF, DOCX, SRT)
- Implementación de diarización (separación de hablantes)
- Marcas de tiempo en transcripciones
- Interfaz con temas personalizables

## 📄 Licencia

MIT License - Ver archivo LICENSE para detalles

## 👨‍💻 Autor

Daniel Ramirez
- GitHub: [@danielcramirez](https://github.com/danielcramirez)

## 🙏 Reconocimientos

- **Vosk**: Motor de reconocimiento de voz
- **Tkinter**: Framework de GUI
- **Comunidad Python**: Por las excelentes bibliotecas

## 📊 Estadísticas del Proyecto

- **Lenguaje**: Python
- **Líneas de código**: ~650 (main.py) + ~150 (otros scripts)
- **Archivos Python**: 3
- **Archivos de documentación**: 4
- **Dependencias**: 6 principales
- **Cobertura de pruebas**: Core functionality
- **Plataformas**: Windows, macOS, Linux

## 🎓 Casos de Uso

1. **Transcripción de entrevistas**
2. **Subtitulado de videos**
3. **Transcripción de reuniones**
4. **Documentación de podcasts**
5. **Accesibilidad (convertir audio en texto para personas con discapacidad auditiva)**
6. **Análisis de contenido hablado**
7. **Creación de documentos a partir de dictados**

## 🔮 Roadmap Futuro

### Versión 1.1 (Potencial)
- [ ] Soporte para más formatos de audio (MP3, M4A, FLAC)
- [ ] Exportación a múltiples formatos
- [ ] Configuración persistente de preferencias

### Versión 1.2 (Potencial)
- [ ] Procesamiento batch
- [ ] Vista previa de audio
- [ ] Atajos de teclado

### Versión 2.0 (Potencial)
- [ ] Diarización de hablantes
- [ ] Timestamps automáticos
- [ ] API REST para integración

---

**Última actualización**: Diciembre 2024
**Versión**: 1.0.0
**Estado**: Producción ✅

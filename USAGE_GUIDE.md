# Guía de Uso - AudioATexto

## Inicio Rápido

### 1. Preparación del Sistema

Antes de usar la aplicación, verifica que tu sistema esté configurado correctamente:

```bash
python check_system.py
```

Este script te dirá si tienes todas las dependencias instaladas y si el modelo de Vosk está presente.

### 2. Flujo de Trabajo Típico

#### Paso 1: Preparar el audio
- Asegúrate de que tu archivo de audio esté en formato WAV o OGG
- Para mejores resultados, usa audio con:
  - Voz clara en español
  - Mínimo ruido de fondo
  - Frecuencia de muestreo de al menos 16 kHz

#### Paso 2: Iniciar la aplicación
```bash
python main.py
```

#### Paso 3: Cargar el audio
1. Haz clic en el botón "Seleccionar Audio"
2. Navega hasta tu archivo de audio
3. Selecciona el archivo (WAV o OGG)

#### Paso 4: Configurar opciones
- **Reducción de ruido**: Recomendado para audios con ruido de fondo
- **Mejora de audio**: Aplica filtros para optimizar frecuencias de voz

#### Paso 5: Transcribir
1. Haz clic en "Iniciar Transcripción"
2. Espera mientras el audio se procesa (verás el progreso en la barra)
3. El texto transcrito aparecerá en el área de resultados

#### Paso 6: Exportar
1. Haz clic en "Exportar a TXT"
2. Elige la ubicación y nombre del archivo
3. Guarda tu transcripción

## Consejos para Mejores Resultados

### Calidad del Audio
- **Óptimo**: Audio grabado en estudio, sin ruido
- **Bueno**: Audio de videollamada o podcast con buena calidad
- **Aceptable**: Grabaciones con algo de ruido de fondo
- **Problemático**: Audio con mucho eco, ruido o voces superpuestas

### Opciones de Procesamiento

#### Cuándo usar reducción de ruido:
- ✅ Audio con ruido de fondo constante (ventilador, tráfico, etc.)
- ✅ Grabaciones en ambientes ruidosos
- ❌ Audio ya limpio (puede reducir calidad)

#### Cuándo usar mejora de audio:
- ✅ Audio con voces lejanas o poco claras
- ✅ Grabaciones con mala calidad de micrófono
- ✅ Audio con frecuencias no optimizadas
- ❌ Audio profesional ya optimizado

### Tamaño y Duración del Audio
- **Archivos pequeños** (< 5 min): Procesamiento rápido (~2-3 min)
- **Archivos medianos** (5-15 min): Procesamiento moderado (~5-10 min)
- **Archivos grandes** (> 15 min): Puede tardar considerable tiempo

**Tip**: Para archivos muy grandes, considera dividirlos en partes más pequeñas.

## Solución de Problemas Comunes

### No se detecta texto
**Problema**: La transcripción está vacía o casi vacía

**Soluciones**:
1. Verifica que el audio contenga voz en español
2. Activa las opciones de mejora de audio
3. Verifica que el volumen del audio sea adecuado
4. Prueba con el modelo completo (vosk-model-es) en vez del pequeño

### Transcripción incorrecta
**Problema**: El texto tiene muchos errores

**Soluciones**:
1. Usa el modelo completo (vosk-model-es) para mayor precisión
2. Activa la reducción de ruido si hay ruido de fondo
3. Verifica que el audio sea claro y audible
4. Asegúrate de que el audio esté en español

### La aplicación se congela
**Problema**: La interfaz no responde durante la transcripción

**Explicación**: Esto es normal. El procesamiento de audio es intensivo y puede tomar tiempo. La barra de progreso se actualizará periódicamente.

**No cierres la aplicación** mientras la barra de progreso esté avanzando.

### Error al cargar el modelo
**Problema**: "No se encontró el modelo de Vosk"

**Soluciones**:
1. Descarga el modelo desde https://alphacephei.com/vosk/models
2. Extrae el archivo ZIP
3. Renombra la carpeta a "model"
4. Colócala en el mismo directorio que main.py

### Error de memoria
**Problema**: "MemoryError" o la aplicación se cierra inesperadamente

**Soluciones**:
1. Usa el modelo pequeño (vosk-model-small-es)
2. Procesa archivos más pequeños
3. Cierra otras aplicaciones para liberar RAM

## Formatos de Audio Soportados

### WAV (.wav)
- ✅ Soporte nativo
- ✅ No requiere conversión
- ✅ Procesamiento más rápido
- Recomendado para mejor rendimiento

### OGG (.ogg)
- ✅ Soporte mediante conversión automática
- ⚠️ Requiere conversión temporal a WAV
- ⚠️ Procesamiento ligeramente más lento
- Compatible pero WAV es preferible

## Requisitos del Sistema

### Mínimos
- CPU: Procesador de 2 núcleos
- RAM: 2 GB disponibles
- Espacio: 100 MB + tamaño del modelo (40 MB - 1.4 GB)
- SO: Windows 7+, macOS 10.12+, Linux (cualquier distribución moderna)

### Recomendados
- CPU: Procesador de 4+ núcleos
- RAM: 4+ GB disponibles
- Espacio: 2 GB disponibles
- SO: Windows 10+, macOS 11+, Ubuntu 20.04+

## Preguntas Frecuentes

**P: ¿Funciona con otros idiomas además del español?**
R: Sí, pero necesitas descargar el modelo correspondiente para tu idioma desde el sitio de Vosk.

**P: ¿Puedo procesar múltiples archivos a la vez?**
R: No, la aplicación procesa un archivo a la vez. Usa el botón "Limpiar" para cargar un nuevo archivo.

**P: ¿Los audios se envían a internet?**
R: No, todo el procesamiento es local. Tus audios nunca salen de tu computadora.

**P: ¿Funciona sin conexión a internet?**
R: Sí, una vez instaladas las dependencias y descargado el modelo, funciona completamente offline.

**P: ¿Puedo usar esto comercialmente?**
R: Verifica las licencias de Vosk y las dependencias. La aplicación en sí está bajo licencia MIT.

## Contacto y Soporte

Para reportar problemas o sugerir mejoras:
- Abre un issue en: https://github.com/danielcramirez/AudioATexto/issues

## Actualizaciones

Para actualizar la aplicación:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

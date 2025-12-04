# Descripción de la Interfaz - AudioATexto

## Estructura de la Interfaz Gráfica

La aplicación AudioATexto cuenta con una interfaz gráfica intuitiva desarrollada con Tkinter que incluye los siguientes elementos:

### 1. Título Principal
```
┌─────────────────────────────────────────────────────────┐
│  AudioATexto - Transcripción de Audio                   │
└─────────────────────────────────────────────────────────┘
```

### 2. Panel de Selección de Archivo
```
┌─ Archivo de Audio ───────────────────────────────────┐
│ [Ruta del archivo........................] [Seleccionar Audio] │
└──────────────────────────────────────────────────────┘
```
- Campo de texto (solo lectura) que muestra la ruta del archivo seleccionado
- Botón "Seleccionar Audio" para abrir el diálogo de selección de archivos

### 3. Panel de Opciones de Procesamiento
```
┌─ Opciones de Procesamiento ──────────────────────────┐
│ [✓] Aplicar reducción de ruido                       │
│ [✓] Aplicar mejora de audio (filtro pasa-banda)      │
└──────────────────────────────────────────────────────┘
```
- Checkbox para activar/desactivar la reducción de ruido
- Checkbox para activar/desactivar la mejora de audio

### 4. Botones de Acción
```
[Iniciar Transcripción]  [Limpiar]  [Exportar a TXT]
```
- **Iniciar Transcripción**: Comienza el proceso de transcripción
- **Limpiar**: Limpia todos los campos y reinicia la aplicación
- **Exportar a TXT**: Guarda la transcripción en un archivo de texto

### 5. Panel de Resultados
```
┌─ Transcripción ──────────────────────────────────────┐
│                                                       │
│  Aquí aparecerá el texto transcrito...               │
│                                                       │
│  [Área de texto con scroll vertical]                 │
│                                                       │
│                                                       │
└──────────────────────────────────────────────────────┘
```
- Área de texto grande con scroll para mostrar la transcripción
- Fuente legible (Arial, tamaño 11)
- Permite seleccionar y copiar el texto

### 6. Barra de Progreso
```
[████████████░░░░░░░░░░░░░] 50%
```
- Muestra el progreso de la transcripción en tiempo real
- Se actualiza durante el procesamiento del audio

### 7. Barra de Estado
```
Estado: Transcribiendo audio... / Listo / Error, etc.
```
- Muestra mensajes informativos sobre el estado actual
- Proporciona feedback al usuario sobre lo que está sucediendo

## Características de la Interfaz

### Diseño Responsivo
- La ventana es redimensionable
- El área de transcripción se expande con la ventana
- Tamaño inicial: 900x700 píxeles

### Feedback Visual
- Botones se deshabilitan cuando no están disponibles
- La barra de progreso muestra el avance
- Mensajes de estado claros y descriptivos
- Diálogos de confirmación y error informativos

### Experiencia de Usuario
- **No bloqueante**: El procesamiento se ejecuta en un hilo separado
- **Intuitivo**: Flujo de trabajo lineal y claro
- **Informativo**: Mensajes claros en cada paso
- **Tolerante a errores**: Manejo de errores con mensajes descriptivos

## Flujo de Interacción

### Secuencia Normal de Uso

1. **Inicio**
   - Usuario ve la ventana principal
   - Estado: "Listo. Seleccione un archivo de audio."
   - Botón "Iniciar Transcripción" deshabilitado

2. **Selección de Archivo**
   - Usuario hace clic en "Seleccionar Audio"
   - Se abre diálogo de selección de archivos
   - Usuario selecciona un archivo WAV o OGG
   - La ruta aparece en el campo de texto
   - Estado: "Archivo seleccionado: [nombre_archivo]"
   - Botón "Iniciar Transcripción" se habilita

3. **Configuración (Opcional)**
   - Usuario marca/desmarca opciones de procesamiento
   - Por defecto, ambas opciones están activadas

4. **Transcripción**
   - Usuario hace clic en "Iniciar Transcripción"
   - Botón se deshabilita
   - Mensajes de estado informativos:
     * "Cargando modelo de reconocimiento de voz..."
     * "Cargando archivo de audio..."
     * "Aplicando reducción de ruido..."
     * "Aplicando filtro de mejora..."
     * "Remuestreando audio a 16kHz..."
     * "Transcribiendo audio..."
   - Barra de progreso se actualiza periódicamente
   - El texto transcrito aparece en el área de resultados
   - Estado: "Transcripción completada exitosamente."
   - Botón "Exportar a TXT" se habilita

5. **Exportación**
   - Usuario hace clic en "Exportar a TXT"
   - Se abre diálogo para guardar archivo
   - Usuario elige ubicación y nombre
   - Archivo se guarda con codificación UTF-8
   - Mensaje de confirmación

6. **Limpieza (Opcional)**
   - Usuario hace clic en "Limpiar"
   - Todos los campos se limpian
   - Aplicación vuelve al estado inicial

## Códigos de Color y Estilo

### Tema
- **Fondo**: Colores del sistema (nativo de Tkinter)
- **Botones**: Estilo ttk (nativo, se adapta al SO)
- **Texto**: Negro sobre fondo blanco
- **Bordes**: Frames con labelframes para mejor organización

### Fuentes
- **Título**: Arial, 16pt, negrita
- **Texto de transcripción**: Arial, 11pt, normal
- **Etiquetas**: Sistema por defecto

## Compatibilidad

### Sistemas Operativos
- ✅ Windows (7, 8, 10, 11)
- ✅ macOS (10.12+)
- ✅ Linux (todas las distribuciones con Tkinter)

### Resoluciones
- **Mínima**: 1024x768
- **Recomendada**: 1920x1080 o superior

### Accesibilidad
- Controles navegables con teclado
- Tamaños de fuente legibles
- Contraste adecuado
- Mensajes de error descriptivos

## Características Técnicas de la GUI

### Threading
- El procesamiento de audio se ejecuta en un hilo separado
- La interfaz permanece responsiva durante la transcripción
- Actualizaciones periódicas desde el hilo de trabajo

### Manejo de Eventos
- Botones con callbacks claros
- Validación de archivos antes de procesar
- Diálogos de confirmación para acciones importantes

### Gestión de Estado
- Variables de control para checkboxes
- Variables de texto para campos de entrada
- Estado de botones se actualiza según el contexto

## Mejoras Futuras Potenciales

1. **Tema oscuro**: Opción para cambiar entre temas claro/oscuro
2. **Historial**: Lista de archivos procesados recientemente
3. **Marcas de tiempo**: Agregar timestamps en la transcripción
4. **Vista previa**: Reproducir el audio seleccionado
5. **Batch processing**: Procesar múltiples archivos
6. **Exportación avanzada**: Más formatos (PDF, DOCX, SRT)
7. **Configuración**: Guardar preferencias del usuario
8. **Atajos de teclado**: Ctrl+O para abrir, Ctrl+S para guardar, etc.

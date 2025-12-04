#!/usr/bin/env python3
"""
AudioATexto - Aplicación GUI para transcripción de audio usando Vosk
Autor: Daniel Ramirez
Descripción: Aplicación de transcripción de audio a texto en español usando Vosk.
            Soporta archivos WAV y OGG, con funciones de mejora de audio,
            reducción de ruido y exportación a texto.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import os
import json
import threading
import wave
import tempfile
from pathlib import Path

try:
    from vosk import Model, KaldiRecognizer
    import soundfile as sf
    import numpy as np
    import noisereduce as nr
    from pydub import AudioSegment
    from scipy import signal
except ImportError as e:
    print(f"Error al importar dependencias: {e}")
    print("Por favor, instala las dependencias: pip install -r requirements.txt")
    exit(1)


class AudioTranscriptionApp:
    """Aplicación principal de transcripción de audio"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("AudioATexto - Transcripción de Audio a Texto")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Variables
        self.audio_file_path = None
        self.transcription_text = ""
        self.model = None
        self.is_transcribing = False
        self.temp_wav_file = None
        
        # Configurar la interfaz
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar peso de las filas y columnas
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Título
        title_label = ttk.Label(
            main_frame, 
            text="AudioATexto - Transcripción de Audio",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Frame para selección de archivo
        file_frame = ttk.LabelFrame(main_frame, text="Archivo de Audio", padding="10")
        file_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(0, weight=1)
        
        # Entry para mostrar la ruta del archivo
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, state="readonly")
        file_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Botón para seleccionar archivo
        select_button = ttk.Button(
            file_frame, 
            text="Seleccionar Audio",
            command=self.select_audio_file
        )
        select_button.grid(row=0, column=1)
        
        # Frame para opciones de mejora de audio
        options_frame = ttk.LabelFrame(main_frame, text="Opciones de Procesamiento", padding="10")
        options_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Checkbox para reducción de ruido
        self.noise_reduction_var = tk.BooleanVar(value=True)
        noise_checkbox = ttk.Checkbutton(
            options_frame,
            text="Aplicar reducción de ruido",
            variable=self.noise_reduction_var
        )
        noise_checkbox.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        # Checkbox para mejora de audio
        self.audio_enhancement_var = tk.BooleanVar(value=True)
        enhancement_checkbox = ttk.Checkbutton(
            options_frame,
            text="Aplicar mejora de audio (filtro pasa-banda)",
            variable=self.audio_enhancement_var
        )
        enhancement_checkbox.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # Frame para botones de acción
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=3, column=0, pady=(0, 10))
        
        # Botón de transcripción
        self.transcribe_button = ttk.Button(
            action_frame,
            text="Iniciar Transcripción",
            command=self.start_transcription,
            state="disabled"
        )
        self.transcribe_button.grid(row=0, column=0, padx=5)
        
        # Botón para limpiar
        clear_button = ttk.Button(
            action_frame,
            text="Limpiar",
            command=self.clear_all
        )
        clear_button.grid(row=0, column=1, padx=5)
        
        # Botón para exportar
        self.export_button = ttk.Button(
            action_frame,
            text="Exportar a TXT",
            command=self.export_to_text,
            state="disabled"
        )
        self.export_button.grid(row=0, column=2, padx=5)
        
        # Frame para resultados
        results_frame = ttk.LabelFrame(main_frame, text="Transcripción", padding="10")
        results_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Área de texto para mostrar la transcripción
        self.transcription_area = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            font=("Arial", 11),
            height=15
        )
        self.transcription_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Barra de progreso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        self.progress_bar.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(10, 5))
        
        # Label de estado
        self.status_var = tk.StringVar(value="Listo. Seleccione un archivo de audio.")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.grid(row=6, column=0, pady=(0, 10))
        
    def select_audio_file(self):
        """Permite al usuario seleccionar un archivo de audio"""
        filetypes = (
            ('Archivos de Audio', '*.wav *.ogg'),
            ('WAV files', '*.wav'),
            ('OGG files', '*.ogg'),
            ('Todos los archivos', '*.*')
        )
        
        filename = filedialog.askopenfilename(
            title='Seleccionar archivo de audio',
            filetypes=filetypes
        )
        
        if filename:
            self.audio_file_path = filename
            self.file_path_var.set(filename)
            self.transcribe_button.config(state="normal")
            self.status_var.set(f"Archivo seleccionado: {os.path.basename(filename)}")
            
    def clear_all(self):
        """Limpia todos los campos y reinicia la aplicación"""
        self.audio_file_path = None
        self.transcription_text = ""
        self.file_path_var.set("")
        self.transcription_area.delete(1.0, tk.END)
        self.progress_var.set(0)
        self.transcribe_button.config(state="disabled")
        self.export_button.config(state="disabled")
        self.status_var.set("Listo. Seleccione un archivo de audio.")
        
    def load_vosk_model(self):
        """Carga el modelo de Vosk para español"""
        try:
            self.status_var.set("Cargando modelo de reconocimiento de voz...")
            self.root.update()
            
            # Buscar modelo en directorios comunes
            model_paths = [
                "model",
                "vosk-model-es",
                "vosk-model-small-es",
                os.path.expanduser("~/vosk-model-es"),
                os.path.expanduser("~/vosk-model-small-es"),
                "/usr/share/vosk/model"
            ]
            
            model_path = None
            for path in model_paths:
                if os.path.exists(path):
                    model_path = path
                    break
            
            if model_path is None:
                messagebox.showerror(
                    "Error",
                    "No se encontró el modelo de Vosk.\n\n"
                    "Por favor, descargue un modelo en español desde:\n"
                    "https://alphacephei.com/vosk/models\n\n"
                    "Extráigalo en el directorio de la aplicación y renómbrelo a 'model'"
                )
                return False
            
            self.model = Model(model_path)
            self.status_var.set("Modelo cargado correctamente.")
            return True
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al cargar el modelo de Vosk:\n{str(e)}"
            )
            return False
    
    def enhance_audio(self, audio_data, sample_rate):
        """Aplica mejoras al audio antes de la transcripción"""
        try:
            enhanced_audio = audio_data.copy()
            
            # Reducción de ruido
            if self.noise_reduction_var.get():
                self.status_var.set("Aplicando reducción de ruido...")
                self.root.update()
                enhanced_audio = nr.reduce_noise(
                    y=enhanced_audio,
                    sr=sample_rate,
                    prop_decrease=0.8
                )
            
            # Filtro pasa-banda para mejorar la voz humana (300 Hz - 3400 Hz)
            if self.audio_enhancement_var.get():
                self.status_var.set("Aplicando filtro de mejora...")
                self.root.update()
                nyquist = sample_rate / 2
                low = 300 / nyquist
                high = 3400 / nyquist
                
                # Validar que las frecuencias estén en el rango válido
                if low < high < 1.0 and low > 0:
                    # Crear filtro Butterworth pasa-banda
                    b, a = signal.butter(4, [low, high], btype='band')
                    enhanced_audio = signal.filtfilt(b, a, enhanced_audio)
                else:
                    # Si el sample rate es muy bajo, usar un filtro pasa-alto simple
                    if low < 1.0:
                        b, a = signal.butter(4, low, btype='high')
                        enhanced_audio = signal.filtfilt(b, a, enhanced_audio)
            
            # Normalizar audio
            max_val = np.max(np.abs(enhanced_audio))
            if max_val > 0:
                enhanced_audio = enhanced_audio / max_val * 0.95
            
            return enhanced_audio
            
        except Exception as e:
            messagebox.showwarning(
                "Advertencia",
                f"No se pudo aplicar mejora de audio:\n{str(e)}\n\n"
                "Continuando con el audio original..."
            )
            return audio_data
    
    def convert_to_wav(self, input_file):
        """Convierte el archivo de audio a formato WAV si es necesario"""
        try:
            file_ext = os.path.splitext(input_file)[1].lower()
            
            if file_ext == '.wav':
                return input_file
            
            # Convertir OGG a WAV
            self.status_var.set("Convirtiendo audio a formato WAV...")
            self.root.update()
            
            audio = AudioSegment.from_file(input_file)
            
            # Convertir a mono y 16kHz para Vosk
            audio = audio.set_channels(1)
            audio = audio.set_frame_rate(16000)
            
            # Guardar temporalmente usando tempfile para compatibilidad cross-platform
            if self.temp_wav_file and os.path.exists(self.temp_wav_file):
                try:
                    os.remove(self.temp_wav_file)
                except:
                    pass
            
            # Crear archivo temporal
            fd, self.temp_wav_file = tempfile.mkstemp(suffix='.wav')
            os.close(fd)
            audio.export(self.temp_wav_file, format='wav')
            
            return self.temp_wav_file
            
        except Exception as e:
            raise Exception(f"Error al convertir audio: {str(e)}")
    
    def transcribe_audio(self):
        """Realiza la transcripción del audio usando Vosk"""
        try:
            # Cargar modelo si no está cargado
            if self.model is None:
                if not self.load_vosk_model():
                    return
            
            # Convertir a WAV si es necesario
            wav_file = self.convert_to_wav(self.audio_file_path)
            
            # Leer archivo de audio
            self.status_var.set("Cargando archivo de audio...")
            self.root.update()
            
            audio_data, sample_rate = sf.read(wav_file)
            
            # Convertir a mono si es estéreo
            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=1)
            
            # Aplicar mejoras de audio
            if self.noise_reduction_var.get() or self.audio_enhancement_var.get():
                audio_data = self.enhance_audio(audio_data, sample_rate)
            
            # Convertir a 16kHz si es necesario (Vosk requiere 16kHz)
            if sample_rate != 16000:
                self.status_var.set("Remuestreando audio a 16kHz...")
                self.root.update()
                num_samples = int(len(audio_data) * 16000 / sample_rate)
                audio_data = signal.resample(audio_data, num_samples)
                sample_rate = 16000
            
            # Convertir a int16 con clipping para evitar overflow
            audio_data = np.clip(audio_data, -1.0, 1.0)
            audio_data = np.int16(audio_data * 32767)
            
            # Crear reconocedor
            rec = KaldiRecognizer(self.model, sample_rate)
            rec.SetWords(True)
            
            # Procesar audio en chunks
            self.status_var.set("Transcribiendo audio...")
            self.root.update()
            
            chunk_size = 4000
            total_chunks = len(audio_data) // chunk_size
            transcription_parts = []
            
            for i in range(0, len(audio_data), chunk_size):
                if not self.is_transcribing:
                    break
                    
                chunk = audio_data[i:i+chunk_size]
                
                if rec.AcceptWaveform(chunk.tobytes()):
                    result = json.loads(rec.Result())
                    if 'text' in result and result['text']:
                        transcription_parts.append(result['text'])
                
                # Actualizar barra de progreso
                progress = (i / len(audio_data)) * 100
                self.progress_var.set(progress)
                self.root.update()
            
            # Obtener resultado final
            final_result = json.loads(rec.FinalResult())
            if 'text' in final_result and final_result['text']:
                transcription_parts.append(final_result['text'])
            
            # Unir todas las partes de la transcripción
            self.transcription_text = ' '.join(transcription_parts)
            
            # Mostrar resultado
            self.transcription_area.delete(1.0, tk.END)
            self.transcription_area.insert(1.0, self.transcription_text)
            
            self.progress_var.set(100)
            
            if self.transcription_text.strip():
                self.status_var.set("Transcripción completada exitosamente.")
                self.export_button.config(state="normal")
            else:
                self.status_var.set("No se detectó texto en el audio.")
                messagebox.showinfo(
                    "Información",
                    "No se pudo detectar texto en el audio.\n"
                    "Verifique que el audio contenga voz en español."
                )
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error durante la transcripción:\n{str(e)}"
            )
            self.status_var.set("Error en la transcripción.")
        
        finally:
            self.is_transcribing = False
            self.transcribe_button.config(state="normal")
            
            # Limpiar archivo temporal si existe
            if self.temp_wav_file and os.path.exists(self.temp_wav_file):
                try:
                    os.remove(self.temp_wav_file)
                    self.temp_wav_file = None
                except:
                    pass
    
    def start_transcription(self):
        """Inicia el proceso de transcripción en un hilo separado"""
        if not self.audio_file_path:
            messagebox.showwarning(
                "Advertencia",
                "Por favor, seleccione un archivo de audio primero."
            )
            return
        
        if not os.path.exists(self.audio_file_path):
            messagebox.showerror(
                "Error",
                "El archivo seleccionado no existe."
            )
            return
        
        # Deshabilitar botón durante la transcripción
        self.transcribe_button.config(state="disabled")
        self.is_transcribing = True
        self.progress_var.set(0)
        self.transcription_area.delete(1.0, tk.END)
        
        # Ejecutar transcripción en un hilo separado
        thread = threading.Thread(target=self.transcribe_audio, daemon=True)
        thread.start()
    
    def export_to_text(self):
        """Exporta la transcripción a un archivo de texto"""
        if not self.transcription_text.strip():
            messagebox.showwarning(
                "Advertencia",
                "No hay transcripción para exportar."
            )
            return
        
        # Sugerir nombre de archivo basado en el audio
        default_name = "transcripcion.txt"
        if self.audio_file_path:
            audio_name = os.path.splitext(os.path.basename(self.audio_file_path))[0]
            default_name = f"{audio_name}_transcripcion.txt"
        
        filename = filedialog.asksaveasfilename(
            title="Guardar transcripción",
            defaultextension=".txt",
            initialfile=default_name,
            filetypes=(
                ("Archivos de texto", "*.txt"),
                ("Todos los archivos", "*.*")
            )
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.transcription_text)
                
                messagebox.showinfo(
                    "Éxito",
                    f"Transcripción guardada correctamente en:\n{filename}"
                )
                self.status_var.set(f"Transcripción exportada: {os.path.basename(filename)}")
                
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Error al guardar el archivo:\n{str(e)}"
                )


def main():
    """Función principal para iniciar la aplicación"""
    root = tk.Tk()
    app = AudioTranscriptionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

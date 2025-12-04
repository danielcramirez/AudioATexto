import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import os
import sys
import wave
import json
import noisereduce as nr
import numpy as np
import soundfile as sf
from vosk import Model, KaldiRecognizer
from pyAudioAnalysis import audioSegmentation as aS
from pydub import AudioSegment

# ----------------------------
# Cargar modelo de Vosk
# ----------------------------
# Detectar si estamos ejecutando desde PyInstaller
if getattr(sys, 'frozen', False):
    # Ejecutando desde el .exe
    base_path = sys._MEIPASS
else:
    # Ejecutando desde Python normal
    base_path = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(base_path, "model")
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"No se encuentra la carpeta 'model' con el modelo Vosk en: {MODEL_PATH}")

model = Model(MODEL_PATH)


# ------------------------------------
# Función para reducir ruido del audio
# ------------------------------------
def mejorar_audio(audio_path):
    data, rate = sf.read(audio_path)
    reduced_noise = nr.reduce_noise(y=data, sr=rate)
    base, ext = os.path.splitext(audio_path)
    out_path = f"{base}_clean.wav"
    sf.write(out_path, reduced_noise, rate)
    return out_path


# ------------------------------------
# Verificar calidad del audio
# ------------------------------------
def verificar_calidad(audio_path):
    try:
        data, rate = sf.read(audio_path)
        rms = np.sqrt(np.mean(data ** 2))
        if rms < 0.01:
            return "Calidad baja: volumen muy bajo."
        elif rms > 0.5:
            return "Calidad regular: posible saturación."
        else:
            return "Calidad buena: señal adecuada."
    except Exception as e:
        return f"Error analizando audio: {e}"


# ------------------------------------
# Diarización (identificación de voces)
# ------------------------------------
def identificar_voces(audio_path):
    try:
        segments, speakers = aS.speaker_diarization(audio_path, 2)
        return speakers
    except Exception:
        return "No se pudo hacer diarización, audio muy corto o ruidoso."


# ------------------------------------
# Transcribir audio
# ------------------------------------
def transcribir(audio_path, text_box):
    temp_wav = None
    if not audio_path.lower().endswith(".wav"):
        try:
            text_box.insert(tk.END, "Convirtiendo audio a WAV...\n")
            text_box.update()
            audio = AudioSegment.from_file(audio_path)
            temp_wav = "temp_converted.wav"
            audio.export(temp_wav, format="wav")
            audio_path = temp_wav
        except Exception as e:
            text_box.insert(tk.END, f"Error convirtiendo audio: {e}\n")
            return ""

    try:
        wf = wave.open(audio_path, "rb")
    except Exception as e:
        text_box.insert(tk.END, f"Error abriendo archivo de audio: {e}\n")
        return ""
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    text_box.insert(tk.END, "Iniciando transcripción...\n")
    text_box.update()

    result_text = ""

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break

        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            if "text" in result:
                line = result["text"] + "\n"
                text_box.insert(tk.END, line)
                text_box.update()
                result_text += line

    final = json.loads(rec.FinalResult())
    if "text" in final:
        text_box.insert(tk.END, "\nFIN DE TRANSCRIPCIÓN\n")
        result_text += final["text"]

    if temp_wav and os.path.exists(temp_wav):
        try:
            os.remove(temp_wav)
        except:
            pass

    return result_text


# ------------------------------------
# Interfaz gráfica
# ------------------------------------

def seleccionar_audio():
    global audio_file
    audio_file = filedialog.askopenfilename(
        title="Seleccionar archivo de audio",
        filetypes=[("Archivos de Audio", "*.wav *.ogg"), ("Archivos WAV", "*.wav"), ("Archivos OGG", "*.ogg")]
    )

    if audio_file:
        text_box.insert(tk.END, f"Audio seleccionado: {audio_file}\n\n")


def procesar_transcripcion():
    if not audio_file:
        messagebox.showerror("Error", "Debe seleccionar un archivo de audio.")
        return

    text_box.delete(1.0, tk.END)
    resultado = transcribir(audio_file, text_box)

    if resultado:
        base_name = os.path.splitext(audio_file)[0]
        txt_path = f"{base_name}_transcripcion.txt"
        try:
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(resultado)
            messagebox.showinfo("Éxito", f"Transcripción guardada en:\n{txt_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo de texto: {e}")


def procesar_mejora():
    if not audio_file:
        messagebox.showerror("Error", "Debe seleccionar un archivo de audio.")
        return

    mejorado = mejorar_audio(audio_file)
    text_box.insert(tk.END, f"Audio mejorado generado: {mejorado}\n\n")


def procesar_calidad():
    if not audio_file:
        messagebox.showerror("Error", "Debe seleccionar un archivo de audio.")
        return

    calidad = verificar_calidad(audio_file)
    text_box.insert(tk.END, f"Calidad del audio: {calidad}\n\n")


def procesar_voces():
    if not audio_file:
        messagebox.showerror("Error", "Debe seleccionar un archivo de audio.")
        return

    resultado = identificar_voces(audio_file)
    text_box.insert(tk.END, f"Voces identificadas: {resultado}\n\n")


# ------------------------------------
# Ventana principal
# ------------------------------------

root = tk.Tk()
root.title("Transcriptor GPLv3 - Español")
root.geometry("800x600")

audio_file = None

btn_select = tk.Button(root, text="Seleccionar Audio", command=seleccionar_audio, width=30)
btn_select.pack(pady=10)

btn_quality = tk.Button(root, text="Verificar Calidad", command=procesar_calidad, width=30)
btn_quality.pack(pady=10)

btn_improve = tk.Button(root, text="Mejorar Audio (Eliminar Ruido)", command=procesar_mejora, width=30)
btn_improve.pack(pady=10)

btn_speakers = tk.Button(root, text="Identificar Voces", command=procesar_voces, width=30)
btn_speakers.pack(pady=10)

btn_transcribe = tk.Button(root, text="Transcribir Audio", command=procesar_transcripcion, width=30)
btn_transcribe.pack(pady=10)

text_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=20)
text_box.pack(padx=10, pady=10)

root.mainloop()

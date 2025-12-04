from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs
import os

# Collect all vosk data files and DLLs
datas = collect_data_files('vosk')
binaries = collect_dynamic_libs('vosk')

# Add vosk directory itself
import vosk
vosk_path = os.path.dirname(vosk.__file__)
datas += [(vosk_path, 'vosk')]

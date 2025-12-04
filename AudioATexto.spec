# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_dynamic_libs, collect_data_files

# Collect Vosk binaries and data
vosk_binaries = collect_dynamic_libs('vosk')
vosk_datas = collect_data_files('vosk')

# Collect imblearn data files (including VERSION.txt)
imblearn_datas = collect_data_files('imblearn')

# Add imblearn VERSION.txt explicitly
import imblearn
imblearn_path = os.path.dirname(imblearn.__file__)
version_file = os.path.join(imblearn_path, 'VERSION.txt')
if os.path.exists(version_file):
    imblearn_datas.append((version_file, 'imblearn'))

# Combine all datas
all_datas = [('model', 'model')] + vosk_datas + imblearn_datas

a = Analysis(
    ['Audio.py'],
    pathex=[],
    binaries=vosk_binaries,
    datas=all_datas,
    hiddenimports=['vosk', 'imblearn'],
    hookspath=['.'],  # Look for hooks in current directory
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AudioATexto',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['logo.ico'],
)

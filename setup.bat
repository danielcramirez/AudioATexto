@echo off
setlocal
cd /d "%~dp0"

echo ==========================================
echo AudioATexto - Setup automatico
echo ==========================================
echo.

powershell -ExecutionPolicy Bypass -File "%~dp0setup.ps1"
if errorlevel 1 (
  echo.
  echo El setup fallo. Revisa los mensajes anteriores.
  pause
  exit /b 1
)

echo.
echo Setup completado correctamente.
echo Puedes ejecutar la app con:
echo .\.venv312\Scripts\python.exe .\Audio.py
echo.
pause
exit /b 0

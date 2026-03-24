param(
    [switch]$SkipModel,
    [switch]$SkipFFmpeg
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

Write-Host "[1/5] Verificando Python 3.12..."
$python312Available = $false
try {
    & py -3.12 --version | Out-Null
    $python312Available = $true
} catch {
    $python312Available = $false
}

if (-not $python312Available) {
    Write-Host "Python 3.12 no encontrado. Instalando con winget..."
    & winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
}

Write-Host "[2/5] Creando entorno virtual .venv312..."
if (-not (Test-Path ".\.venv312\Scripts\python.exe")) {
    & py -3.12 -m venv .venv312
}

$py = Join-Path $repoRoot ".venv312\Scripts\python.exe"

Write-Host "[3/5] Instalando dependencias de Python..."
& $py -m pip install --upgrade pip
& $py -m pip install -r requirements.txt

if (-not $SkipModel) {
    Write-Host "[4/5] Verificando modelo Vosk..."
    if (-not (Test-Path ".\model\am")) {
        $modelZip = Join-Path $repoRoot "vosk-model-es-0.42.zip"
        $modelUrl = "https://alphacephei.com/vosk/models/vosk-model-es-0.42.zip"
        $modelExtract = Join-Path $repoRoot "_model_extract"

        if (Test-Path $modelExtract) {
            Remove-Item -Recurse -Force $modelExtract
        }

        Write-Host "Descargando modelo Vosk (esto puede tardar)..."
        Invoke-WebRequest -UseBasicParsing -Uri $modelUrl -OutFile $modelZip

        Expand-Archive -Path $modelZip -DestinationPath $modelExtract -Force
        $modelFolder = Get-ChildItem -Path $modelExtract -Directory | Select-Object -First 1

        if (-not $modelFolder) {
            throw "No se encontro carpeta extraida del modelo Vosk"
        }

        if (Test-Path ".\model") {
            Remove-Item -Recurse -Force ".\model"
        }

        Move-Item -Path $modelFolder.FullName -Destination ".\model"
        Remove-Item -Recurse -Force $modelExtract
    }
} else {
    Write-Host "[4/5] Modelo Vosk omitido por parametro -SkipModel"
}

if (-not $SkipFFmpeg) {
    Write-Host "[5/5] Verificando FFmpeg local..."
    if (-not (Test-Path ".\ffmpeg\bin\ffmpeg.exe") -or -not (Test-Path ".\ffmpeg\bin\ffprobe.exe")) {
        $ffmpegZip = Join-Path $repoRoot "ffmpeg-release-essentials.zip"
        $ffmpegUrl = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        $ffmpegExtract = Join-Path $repoRoot "_ffmpeg_extract"

        if (Test-Path $ffmpegExtract) {
            Remove-Item -Recurse -Force $ffmpegExtract
        }

        Write-Host "Descargando FFmpeg (esto puede tardar)..."
        Invoke-WebRequest -UseBasicParsing -Uri $ffmpegUrl -OutFile $ffmpegZip

        Expand-Archive -Path $ffmpegZip -DestinationPath $ffmpegExtract -Force
        $ffmpegFolder = Get-ChildItem -Path $ffmpegExtract -Directory | Select-Object -First 1

        if (-not $ffmpegFolder) {
            throw "No se encontro carpeta extraida de FFmpeg"
        }

        if (Test-Path ".\ffmpeg") {
            Remove-Item -Recurse -Force ".\ffmpeg"
        }

        Move-Item -Path $ffmpegFolder.FullName -Destination ".\ffmpeg"
        Remove-Item -Recurse -Force $ffmpegExtract
    }
} else {
    Write-Host "[5/5] FFmpeg omitido por parametro -SkipFFmpeg"
}

Write-Host ""
Write-Host "Setup completado."
Write-Host "Ejecuta la app con:"
Write-Host ".\.venv312\Scripts\python.exe .\Audio.py"

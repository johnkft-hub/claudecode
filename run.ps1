$ErrorActionPreference = "Stop"
$REPO_URL   = "https://github.com/johnkft-hub/claudecode.git"
$BRANCH     = "claude/attachment-skill-program-tNnGl"
$PROJECT    = Join-Path $PSScriptRoot "claudecode"
$SHORTS     = Join-Path $PROJECT "shorts_maker"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host " Shorts Video Maker - Setup and Run"        -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# Python
try   { $v = python --version 2>&1; Write-Host "[OK] $v" -ForegroundColor Green }
catch { Write-Host "[ERROR] Python not found. Install from https://python.org" -ForegroundColor Red; Read-Host "Press Enter"; exit 1 }

# git
try   { $v = git --version 2>&1; Write-Host "[OK] $v" -ForegroundColor Green }
catch { Write-Host "[ERROR] git not found. Install from https://git-scm.com" -ForegroundColor Red; Read-Host "Press Enter"; exit 1 }

# ffmpeg
try   { ffmpeg -version 2>&1 | Out-Null; Write-Host "[OK] ffmpeg found" -ForegroundColor Green }
catch {
    Write-Host "[WARN] ffmpeg not found. Trying winget install..." -ForegroundColor Yellow
    winget install --id Gyan.FFmpeg -e --silent
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] ffmpeg install failed. Install manually from https://ffmpeg.org" -ForegroundColor Red
        Read-Host "Press Enter"; exit 1
    }
}

# clone or pull
if (Test-Path (Join-Path $PROJECT ".git")) {
    Write-Host "[UPDATE] Pulling latest code..." -ForegroundColor Cyan
    git -C $PROJECT pull origin $BRANCH
} else {
    Write-Host "[DOWNLOAD] Cloning repository..." -ForegroundColor Cyan
    git clone -b $BRANCH $REPO_URL $PROJECT
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Clone failed. Check internet connection." -ForegroundColor Red
        Read-Host "Press Enter"; exit 1
    }
}

# install packages
Write-Host "[INSTALL] Installing Python packages..." -ForegroundColor Cyan
python -m pip install -q -r (Join-Path $SHORTS "requirements.txt")
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Package install failed." -ForegroundColor Red
    Read-Host "Press Enter"; exit 1
}
Write-Host "[OK] Packages installed." -ForegroundColor Green

# font check
$FONT = Join-Path $SHORTS "assets\fonts\NanumGothicBold.ttf"
if (-not (Test-Path $FONT)) {
    Write-Host ""
    Write-Host "[NOTICE] Korean font not found." -ForegroundColor Yellow
    Write-Host "  Copy NanumGothicBold.ttf to:"
    Write-Host "  $($SHORTS)\assets\fonts\"
    Write-Host "  Download: https://hangeul.naver.com/font"
    Write-Host ""
    Read-Host "Press Enter after copying the font"
}

# run
Write-Host "[RUN] Starting application..." -ForegroundColor Green
Set-Location $SHORTS
python gui.py

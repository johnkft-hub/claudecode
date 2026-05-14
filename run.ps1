$ErrorActionPreference = "Stop"
$REPO_URL = "https://github.com/johnkft-hub/claudecode.git"
$BRANCH   = "claude/attachment-skill-program-tNnGl"
$PROJECT  = Join-Path $PSScriptRoot "claudecode"
$SHORTS   = Join-Path $PROJECT "shorts_maker"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host " Shorts Video Maker - Setup and Run"        -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# ── Python 찾기 (PATH 미등록 환경 포함) ──────────────────────────────────
function Find-Python {
    # 1) PATH에 있으면 바로 사용
    $p = Get-Command python -ErrorAction SilentlyContinue
    if ($p) { return $p.Source }

    # 2) 일반적인 설치 경로 탐색
    $candidates = @(
        "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe",
        "C:\Python313\python.exe",
        "C:\Python312\python.exe",
        "C:\Python311\python.exe",
        "C:\Python310\python.exe"
    )
    foreach ($c in $candidates) {
        if (Test-Path $c) { return $c }
    }

    # 3) 드라이브 전체에서 검색 (느릴 수 있음)
    $found = Get-ChildItem "C:\Users\$env:USERNAME\AppData\Local\Programs\Python" `
             -Filter "python.exe" -Recurse -ErrorAction SilentlyContinue |
             Select-Object -First 1 -ExpandProperty FullName
    return $found
}

$PYTHON = Find-Python
if (-not $PYTHON) {
    Write-Host "[ERROR] Python not found." -ForegroundColor Red
    Write-Host "  Install from https://www.python.org"
    Write-Host "  During install, check 'Add Python to PATH'"
    Read-Host "Press Enter to exit"; exit 1
}
$v = & $PYTHON --version 2>&1
Write-Host "[OK] $v  ($PYTHON)" -ForegroundColor Green

# ── git ──────────────────────────────────────────────────────────────────
$GIT = Get-Command git -ErrorAction SilentlyContinue
if (-not $GIT) {
    Write-Host "[ERROR] git not found. Install from https://git-scm.com" -ForegroundColor Red
    Read-Host "Press Enter to exit"; exit 1
}
Write-Host "[OK] $(git --version)" -ForegroundColor Green

# ── ffmpeg ────────────────────────────────────────────────────────────────
$FF = Get-Command ffmpeg -ErrorAction SilentlyContinue
if (-not $FF) {
    Write-Host "[WARN] ffmpeg not found. Trying winget install..." -ForegroundColor Yellow
    winget install --id Gyan.FFmpeg -e --silent
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] ffmpeg install failed." -ForegroundColor Red
        Write-Host "  Download from https://ffmpeg.org and add to PATH"
        Read-Host "Press Enter to exit"; exit 1
    }
    # PATH 갱신
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" +
                [System.Environment]::GetEnvironmentVariable("PATH","User")
}
Write-Host "[OK] ffmpeg found" -ForegroundColor Green

# ── clone or pull ─────────────────────────────────────────────────────────
if (Test-Path (Join-Path $PROJECT ".git")) {
    Write-Host "[UPDATE] Pulling latest code..." -ForegroundColor Cyan
    git -C $PROJECT pull origin $BRANCH
} else {
    Write-Host "[DOWNLOAD] Cloning repository..." -ForegroundColor Cyan
    git clone -b $BRANCH $REPO_URL $PROJECT
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Clone failed. Check internet connection." -ForegroundColor Red
        Read-Host "Press Enter to exit"; exit 1
    }
}

# ── 패키지 설치 ───────────────────────────────────────────────────────────
Write-Host "[INSTALL] Installing Python packages..." -ForegroundColor Cyan
& $PYTHON -m pip install -q -r (Join-Path $SHORTS "requirements.txt")
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Package install failed." -ForegroundColor Red
    Read-Host "Press Enter to exit"; exit 1
}
Write-Host "[OK] Packages installed." -ForegroundColor Green

# ── 한글 폰트 확인 ────────────────────────────────────────────────────────
$FONT = Join-Path $SHORTS "assets\fonts\NanumGothicBold.ttf"
if (-not (Test-Path $FONT)) {
    Write-Host ""
    Write-Host "[NOTICE] Korean font not found." -ForegroundColor Yellow
    Write-Host "  Copy NanumGothicBold.ttf to:"
    Write-Host "  $SHORTS\assets\fonts\"
    Write-Host "  Download: https://hangeul.naver.com/font"
    Write-Host ""
    Read-Host "Press Enter after copying the font"
}

# ── 실행 ─────────────────────────────────────────────────────────────────
Write-Host "[RUN] Starting application..." -ForegroundColor Green
Set-Location $SHORTS
& $PYTHON gui.py

@echo off
setlocal

set REPO_URL=https://github.com/johnkft-hub/claudecode.git
set BRANCH=claude/attachment-skill-program-tNnGl
set PROJECT_DIR=%~dp0claudecode
set SHORTS_DIR=%PROJECT_DIR%\shorts_maker

echo ============================================
echo  Shorts Video Maker - Setup and Run
echo ============================================

:: Python check
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found.
    echo Please install Python 3.10+ from https://www.python.org
    pause
    exit /b 1
)
echo [OK] Python found.

:: git check
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] git not found.
    echo Please install git from https://git-scm.com
    pause
    exit /b 1
)
echo [OK] git found.

:: ffmpeg check
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo [WARN] ffmpeg not found. Trying to install via winget...
    winget install --id Gyan.FFmpeg -e --silent
    if errorlevel 1 (
        echo [ERROR] ffmpeg install failed.
        echo Please install manually from https://ffmpeg.org and add to PATH.
        pause
        exit /b 1
    )
)
echo [OK] ffmpeg found.

:: clone or pull
if exist "%PROJECT_DIR%\.git" (
    echo [UPDATE] Pulling latest code...
    git -C "%PROJECT_DIR%" pull origin %BRANCH%
) else (
    echo [DOWNLOAD] Cloning repository...
    git clone -b %BRANCH% %REPO_URL% "%PROJECT_DIR%"
    if errorlevel 1 (
        echo [ERROR] Clone failed. Check your internet connection.
        pause
        exit /b 1
    )
)

:: install packages
echo [INSTALL] Installing Python packages...
python -m pip install -q -r "%SHORTS_DIR%\requirements.txt"
if errorlevel 1 (
    echo [ERROR] Package install failed.
    pause
    exit /b 1
)
echo [OK] Packages installed.

:: font check
if not exist "%SHORTS_DIR%\assets\fonts\NanumGothicBold.ttf" (
    echo.
    echo [NOTICE] Korean font not found.
    echo Please copy NanumGothicBold.ttf to:
    echo   %SHORTS_DIR%\assets\fonts\
    echo Download: https://hangeul.naver.com/font
    echo.
    pause
)

:: run
echo [RUN] Starting application...
cd /d "%SHORTS_DIR%"
python gui.py

echo.
echo Done.
pause
endlocal

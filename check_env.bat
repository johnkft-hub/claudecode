@echo off
setlocal

echo ============================================
echo  Environment Check
echo ============================================
echo.

echo [1] Python:
python --version
if errorlevel 1 echo     ^^^ NOT FOUND - install from https://python.org
echo.

echo [2] pip:
python -m pip --version
echo.

echo [3] git:
git --version
if errorlevel 1 echo     ^^^ NOT FOUND - install from https://git-scm.com
echo.

echo [4] ffmpeg:
ffmpeg -version 2>&1 | findstr "ffmpeg version"
if errorlevel 1 echo     ^^^ NOT FOUND - install from https://ffmpeg.org
echo.

echo [5] Installed packages:
python -m pip show moviepy pillow gtts edge-tts 2>&1 | findstr "Name Version"
echo.

echo ============================================
echo  Done. Please share a screenshot if issues persist.
echo ============================================
pause
endlocal

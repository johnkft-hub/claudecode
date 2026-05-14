@echo off
chcp 65001 >nul
echo ============================================
echo  환경 진단
echo ============================================
echo.

echo [1] Python 버전:
python --version
if errorlevel 1 echo   ^^^ Python 없음 - https://python.org 에서 설치 필요
echo.

echo [2] pip 버전:
python -m pip --version
echo.

echo [3] git 버전:
git --version
if errorlevel 1 echo   ^^^ git 없음 - https://git-scm.com 에서 설치 필요
echo.

echo [4] ffmpeg 버전:
ffmpeg -version 2>&1 | findstr "ffmpeg version"
if errorlevel 1 echo   ^^^ ffmpeg 없음 - https://ffmpeg.org 에서 설치 필요
echo.

echo [5] 설치된 패키지:
python -m pip show moviepy pillow gtts edge-tts 2>&1 | findstr "Name Version"
echo.

echo ============================================
echo  진단 완료. 위 내용을 캡처해서 공유해주세요.
echo ============================================
pause

@echo off
chcp 65001 >nul
setlocal

set REPO_URL=https://github.com/johnkft-hub/claudecode.git
set PROJECT_DIR=%~dp0claudecode
set SHORTS_DIR=%PROJECT_DIR%\shorts_maker

echo ============================================
echo  쇼츠 영상 제작기 — 설치 및 실행
echo ============================================

:: Python 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo [오류] Python이 설치되어 있지 않습니다.
    echo https://www.python.org 에서 Python 3.10 이상을 설치하세요.
    pause
    exit /b 1
)

:: ffmpeg 확인
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo [경고] ffmpeg가 없습니다. 자동 설치를 시도합니다...
    winget install --id Gyan.FFmpeg -e --silent
    if errorlevel 1 (
        echo [오류] ffmpeg 설치 실패. https://ffmpeg.org 에서 수동 설치 후 재실행하세요.
        pause
        exit /b 1
    )
)

:: 저장소 clone 또는 pull
if exist "%PROJECT_DIR%\.git" (
    echo [업데이트] 최신 코드를 가져옵니다...
    git -C "%PROJECT_DIR%" pull origin claude/attachment-skill-program-tNnGl
) else (
    echo [다운로드] 저장소를 clone 합니다...
    git clone -b claude/attachment-skill-program-tNnGl %REPO_URL% "%PROJECT_DIR%"
    if errorlevel 1 (
        echo [오류] clone 실패. 인터넷 연결을 확인하세요.
        pause
        exit /b 1
    )
)

:: 의존성 설치
echo [설치] 필요한 패키지를 설치합니다...
python -m pip install -q -r "%SHORTS_DIR%\requirements.txt"

:: 한글 폰트 안내
if not exist "%SHORTS_DIR%\assets\fonts\NanumGothicBold.ttf" (
    echo.
    echo [안내] 한글 폰트가 없습니다.
    echo  NanumGothicBold.ttf 를 아래 경로에 복사하세요:
    echo  %SHORTS_DIR%\assets\fonts\
    echo  다운로드: https://hangeul.naver.com/font
    echo.
    pause
)

:: 실행
echo [실행] 프로그램을 시작합니다...
cd /d "%SHORTS_DIR%"
python gui.py

:END
echo.
echo 프로그램이 종료됐습니다.
pause
endlocal

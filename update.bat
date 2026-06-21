@echo off
cd /d "%~dp0"
echo ============================================
echo   Skill Hub - local update
echo ============================================

if not exist "token.local" (
  echo.
  echo [!] token.local NOT found.
  echo     Create a file named  token.local  in this folder,
  echo     put your GitHub token ^(ghp_...^) on ONE line, save, then run again.
  echo.
  pause
  exit /b 1
)

set "GITHUB_TOKEN="
set /p GITHUB_TOKEN=<token.local
if "%GITHUB_TOKEN%"=="" (
  echo [!] token.local is EMPTY. Put your ghp_ token inside it first.
  pause
  exit /b 1
)

echo Crawling GitHub, this may take a few minutes. Do NOT close this window.
echo.
python update_skills.py
set RC=%errorlevel%
echo.
if not "%RC%"=="0" (
  echo [!] FAILED with code %RC%. Common causes: invalid token / network.
  pause
  exit /b %RC%
)

echo Done! Opening the webpage...
start "" "index.html"
pause

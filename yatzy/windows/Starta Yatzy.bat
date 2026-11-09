@echo off
setlocal
rem ====================================================================
rem  Yatzy tillsammans - dubbelklicka den har filen for att starta.
rem  Servern startar i ett eget minimerat fonster. Stang det fonstret
rem  nar ni spelat klart.
rem ====================================================================
cd /d "%~dp0"

rem Python heter olika saker beroende pa hur det installerats.
set "PY="
where py >nul 2>&1 && set "PY=py -3"
if not defined PY where python >nul 2>&1 && set "PY=python"
if not defined PY where python3 >nul 2>&1 && set "PY=python3"

if not defined PY (
  echo.
  echo   Python 3 hittades inte pa den har datorn.
  echo.
  echo   Installera fran:  https://www.python.org/downloads/
  echo   Kryssa i "Add Python to PATH" under installationen,
  echo   starta om datorn och prova igen.
  echo.
  pause
  exit /b 1
)

rem Starta servern i ett eget fonster.
start "Yatzy-server" /min %PY% server.py --no-browser

rem Vanta tills servern faktiskt svarar, annars oppnas en tom sida.
set /a TRIES=0
:wait
set /a TRIES+=1
%PY% -c "import socket,sys;s=socket.socket();s.settimeout(0.4);sys.exit(0 if s.connect_ex(('127.0.0.1',8765))==0 else 1)" >nul 2>&1
if not errorlevel 1 goto ready
if %TRIES% GEQ 25 (
  echo.
  echo   Servern svarar inte. Prova att oppna adressen for hand:
  echo   http://127.0.0.1:8765/
  echo.
  pause
  exit /b 1
)
timeout /t 1 /nobreak >nul
goto wait

:ready
rem Forsta fonstret: skriv in namn och poang.
rem TV-fonstret oppnas av sidan sjalv nar spelet startas.
start "" "http://127.0.0.1:8765/"
exit /b 0

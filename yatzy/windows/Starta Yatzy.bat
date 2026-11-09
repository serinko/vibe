@echo off
setlocal enabledelayedexpansion
title Yatzy tillsammans
cd /d "%~dp0"

echo.
echo   Yatzy tillsammans
echo   -----------------
echo.

rem --- hitta Python ---------------------------------------------------
set "PY="
where py >nul 2>&1
if not errorlevel 1 set "PY=py -3"
if not defined PY (
  where python >nul 2>&1
  if not errorlevel 1 set "PY=python"
)
if not defined PY (
  where python3 >nul 2>&1
  if not errorlevel 1 set "PY=python3"
)

if not defined PY (
  echo   [FEL] Python 3 hittades inte.
  echo.
  echo   Installera fran https://www.python.org/downloads/
  echo   Kryssa i "Add Python to PATH" under installationen,
  echo   starta om datorn och prova igen.
  echo.
  pause
  exit /b 1
)
echo   Python: %PY%

rem --- finns filerna? --------------------------------------------------
if not exist "server.py" (
  echo   [FEL] server.py saknas i den har mappen:
  echo         %CD%
  echo.
  echo   Packa upp hela zip-filen och kor den har filen darifran.
  echo.
  pause
  exit /b 1
)

rem --- starta servern i ett eget fonster --------------------------------
echo   Startar servern...
start "Yatzy-server" %PY% server.py --no-browser

rem --- vanta tills den svarar -------------------------------------------
set /a TRIES=0
:wait
set /a TRIES+=1
%PY% -c "import socket,sys; s=socket.socket(); s.settimeout(0.4); sys.exit(0 if s.connect_ex(('127.0.0.1',8765))==0 else 1)" >nul 2>&1
if not errorlevel 1 goto ready
if !TRIES! GEQ 20 (
  echo.
  echo   [FEL] Servern svarade inte.
  echo   Titta i fonstret "Yatzy-server" - felmeddelandet star dar.
  echo.
  echo   Prova annars att kora for hand i det har fonstret:
  echo       %PY% server.py
  echo.
  pause
  exit /b 1
)
echo   Vantar pa servern... !TRIES!/20
timeout /t 1 /nobreak >nul
goto wait

:ready
echo   Servern ar igang.
echo   Oppnar webblasaren...
start "" "http://127.0.0.1:8765/"
echo.
echo   Klart. Las fonstret "Yatzy-server" vara oppet medan ni spelar.
echo   Det har fonstret kan du stanga.
echo.
timeout /t 5 /nobreak >nul
exit /b 0

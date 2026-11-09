@echo off
rem Stanger Yatzy-servern om fonstret blivit kvar i bakgrunden.
taskkill /FI "WINDOWTITLE eq Yatzy-server*" /T /F >nul 2>&1
echo Yatzy har stangts.
timeout /t 2 /nobreak >nul

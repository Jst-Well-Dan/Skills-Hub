@echo off
setlocal

REM Stop Skills-Hub Admin services (Admin API :5173, static site :5174).
REM ASCII only, see note in start-admin.bat.

echo Stopping Skills-Hub Admin services...

REM Kill processes listening on 5173 / 5174 (works on Win10+; no wmic needed)
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 5173,5174 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }"

REM Fallback: close by window title
taskkill /FI "WINDOWTITLE eq Skills-Hub Admin API*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Skills-Hub Site*" /F >nul 2>&1

echo  Done. If the ports are still busy:
echo    netstat -ano | findstr "5173 5174"
pause
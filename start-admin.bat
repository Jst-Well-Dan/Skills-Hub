@echo off
setlocal enabledelayedexpansion

REM ============================================================
REM  Skills-Hub one-click admin launcher
REM  Starts Admin API (5173) + static site (5174) + opens browser
REM  Project root: %~dp0
REM  NOTE: ASCII only. cmd.exe parses .bat with the system ANSI
REM  codepage (e.g. 936/GBK); UTF-8 Chinese breaks line parsing.
REM ============================================================
cd /d "%~dp0"

set "ADMIN_PORT=5173"
set "SITE_PORT=5174"

echo.
echo  ========================================
echo   Skills-Hub Admin launcher
echo  ========================================
echo.

REM --- 1. Check Python ---
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found. Install Python 3 and add it to PATH.
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('python --version 2^>^&1') do echo  [OK] Python %%v

REM --- 2. Start Admin API (skip if already healthy) ---
powershell -NoProfile -Command "try { $r = Invoke-WebRequest -UseBasicParsing -TimeoutSec 2 -Uri 'http://127.0.0.1:%ADMIN_PORT%/api/health'; if ($r.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1
if %errorlevel%==0 (
    echo  [SKIP] Admin API already running on http://127.0.0.1:%ADMIN_PORT%
    goto :start_site
)

echo  [START] Admin API http://127.0.0.1:%ADMIN_PORT% ...
if exist ".admin.log" del /q ".admin.log" >nul 2>&1
start "Skills-Hub Admin API" /min cmd /c "python scripts\admin_server.py --host 127.0.0.1 --port %ADMIN_PORT% > .admin.log 2>&1"

echo  [WAIT] Waiting for the backend to become ready...
set /a waits=0
:wait_admin
ping -n 2 127.0.0.1 >nul
powershell -NoProfile -Command "try { $r = Invoke-WebRequest -UseBasicParsing -TimeoutSec 1 -Uri 'http://127.0.0.1:%ADMIN_PORT%/api/health'; if ($r.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1
if !errorlevel!==0 (
    echo  [OK] Admin API ready
    goto :start_site
)
set /a waits+=1
if !waits! LSS 10 goto :wait_admin

echo  [WARN] Backend not ready within 10s. Check .admin.log
type ".admin.log" 2>nul
echo.

:start_site
REM --- 3. Start static site (skip if already up) ---
powershell -NoProfile -Command "try { $r = Invoke-WebRequest -UseBasicParsing -TimeoutSec 2 -Uri 'http://127.0.0.1:%SITE_PORT%/index.html'; if ($r.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1
if %errorlevel%==0 (
    echo  [SKIP] Site already running on http://127.0.0.1:%SITE_PORT%
    goto :open_browser
)
echo  [START] Static site http://127.0.0.1:%SITE_PORT% ...
if exist ".site.log" del /q ".site.log" >nul 2>&1
start "Skills-Hub Site" /min cmd /c "python -m http.server %SITE_PORT% --directory site > .site.log 2>&1"
ping -n 3 127.0.0.1 >nul

:open_browser
echo  [OPEN] Browser http://127.0.0.1:%SITE_PORT%/index.html?admin=1
start "" "http://127.0.0.1:%SITE_PORT%/index.html?admin=1"

echo.
echo  ----------------------------------------
echo   Done! Both services are running minimized.
echo   - Admin API : http://127.0.0.1:%ADMIN_PORT%/api/health
echo   - Frontend  : http://127.0.0.1:%SITE_PORT%/index.html?admin=1
echo   - Logs      : .admin.log / .site.log
echo   Closing this window will NOT stop the services.
echo   Run stop-admin.bat to stop them.
echo  ----------------------------------------
echo.
pause
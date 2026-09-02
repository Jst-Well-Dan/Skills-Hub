@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM ============================================================
REM  Skills-Hub 一键启动管理员模式
REM  双击即可：启动后端 API (5173) + 静态站点 (5174) + 打开浏览器
REM  项目根目录: %~dp0
REM ============================================================
cd /d "%~dp0"

echo.
echo  ╔════════════════════════════════════════╗
echo  ║   Skills-Hub Admin 一键启动           ║
echo  ╚════════════════════════════════════════╝
echo.

REM --- 1. 检查 Python ---
python --version >nul 2>&1
if errorlevel 1 (
  echo  [错误] 未找到 python，请先安装 Python 3 并加入 PATH
  echo         当前 PATH: %PATH%
  pause
  exit /b 1
)
for /f "tokens=*" %%v in ('python --version 2^>^&1') do echo  [OK] %%v

REM --- 2. 检查端口是否已被占用（已启动则跳过）---
set ADMIN_PORT=5173
set SITE_PORT=5174

REM 函数：检查 health
powershell -Command "try { $r=Invoke-WebRequest -UseBasicParsing -TimeoutSec 2 http://127.0.0.1:%ADMIN_PORT%/api/health -ErrorAction Stop; if($r.Content -match '\"ok\"'){ exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1
if %errorlevel%==0 (
  echo  [跳过] Admin API 已在运行 http://127.0.0.1:%ADMIN_PORT%
  goto :start_site
)

echo  [启动] Admin API http://127.0.0.1:%ADMIN_PORT% ...
REM 用 start 新窗口最小化运行，日志落在 .admin.log 便于排查
if exist ".admin.log" del /q ".admin.log" >nul 2>&1
start "Skills-Hub Admin API" /min cmd /c "python scripts\admin_server.py --host 127.0.0.1 --port %ADMIN_PORT% > .admin.log 2>&1"

REM 等待最多 10 秒直到 health 就绪
echo  [等待] 等待后端就绪...
for /l %%i in (1,1,10) do (
  timeout /t 1 /nobreak >nul
  powershell -Command "try { $r=Invoke-WebRequest -UseBasicParsing -TimeoutSec 1 http://127.0.0.1:%ADMIN_PORT%/api/health -ErrorAction Stop; if($r.Content -match '\"ok\"'){ exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1
  if !errorlevel!==0 (
    echo  [OK] Admin API 就绪
    goto :start_site
  )
  echo    ...%%i 秒
)
echo  [警告] 后端 10秒内未就绪，请查看 .admin.log
type ".admin.log" 2>nul
echo.

:start_site
REM --- 3. 启动静态站点 ---
powershell -Command "try { $r=Invoke-WebRequest -UseBasicParsing -TimeoutSec 2 http://127.0.0.1:%SITE_PORT%/index.html -ErrorAction Stop; exit 0 } catch { exit 1 }" >nul 2>&1
if %errorlevel%==0 (
  echo  [跳过] Site 已在运行 http://127.0.0.1:%SITE_PORT%
  goto :open_browser
)
echo  [启动] 静态站点 http://127.0.0.1:%SITE_PORT% ...
if exist ".site.log" del /q ".site.log" >nul 2>&1
start "Skills-Hub Site" /min cmd /c "python -m http.server %SITE_PORT% --directory site > .site.log 2>&1"
timeout /t 2 /nobreak >nul

:open_browser
echo  [打开] 浏览器 http://127.0.0.1:%SITE_PORT%/index.html?admin=1
start "" "http://127.0.0.1:%SITE_PORT%/index.html?admin=1"

echo.
echo  ────────────────────────────────────────
echo   已完成！两个服务已在后台最小化运行
echo   - Admin API : http://127.0.0.1:%ADMIN_PORT%/api/health
echo   - 前端入口  : http://127.0.0.1:%SITE_PORT%/index.html?admin=1
echo   - 日志      : .admin.log / .site.log
echo   关闭窗口不会停止服务，需运行 stop-admin.bat
echo  ────────────────────────────────────────
echo.
pause

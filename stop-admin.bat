@echo off
chcp 65001 >nul
echo 正在停止 Skills-Hub Admin 服务...

REM 通过 wmic 查找命令行包含 admin_server.py / http.server 的 python 进程
for /f "tokens=2 delims== " %%a in ('wmic process where "CommandLine like '%%admin_server.py%%'" get ProcessId /value 2^>nul ^| find "ProcessId"') do (
  echo  停止 Admin API PID=%%a
  taskkill /PID %%a /F >nul 2>&1
)
for /f "tokens=2 delims== " %%a in ('wmic process where "CommandLine like '%%http.server%%5174%%'" get ProcessId /value 2^>nul ^| find "ProcessId"') do (
  echo  停止 Site PID=%%a
  taskkill /PID %%a /F >nul 2>&1
)
REM 兜底：按窗口标题关闭
taskkill /FI "WINDOWTITLE eq Skills-Hub Admin API*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Skills-Hub Site*" /F >nul 2>&1

echo  已停止。如仍占用端口，可手动： netstat -ano ^| findstr "5173 5174"
pause

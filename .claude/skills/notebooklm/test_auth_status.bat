@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================
echo       检查 NotebookLM 认证状态
echo ============================================
echo.
python scripts/run.py auth_manager.py status
echo.
echo ============================================
echo 如果显示 "Authenticated: No"，请重新登录
echo 运行 auth_setup.bat 重新登录
echo ============================================
pause

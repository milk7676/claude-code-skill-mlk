@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================
echo            NotebookLM 诊断测试
echo ============================================
echo.
echo 这个测试会：
echo 1. 启动 Chrome 浏览器
echo 2. 访问 Google 主页
echo 3. 访问 NotebookLM
echo.
echo 请观察浏览器是否正常打开和加载页面
echo ============================================
echo.
.venv\Scripts\python.exe diagnose.py
pause

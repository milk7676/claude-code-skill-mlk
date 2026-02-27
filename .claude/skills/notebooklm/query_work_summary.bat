@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================
echo          查询工作总结笔记本
echo ============================================
echo.
echo 问题: 最近的工作重点是什么？请详细列出
echo.
echo ============================================
.venv\Scripts\python.exe -X utf8 scripts\ask_question.py --question "最近的工作重点是什么？请详细列出" --notebook-url "https://notebooklm.google.com/notebook/256b0760-a92f-4fd0-9d84-9a1cd0ace822" --show-browser
echo.
echo ============================================
pause

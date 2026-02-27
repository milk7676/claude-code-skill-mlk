@echo off
chcp 65001 >nul
cd /d "%~dp0"
python scripts/run.py ask_question.py --question "这个工作总结笔记本包含哪些主要内容？" --notebook-url "https://notebooklm.google.com/notebook/256b0760-a92f-4fd0-9d84-9a1cd0ace822" --show-browser --timeout 5
pause

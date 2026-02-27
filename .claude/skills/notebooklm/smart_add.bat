@echo off
chcp 65001 >nul
cd /d "%~dp0"
python scripts/run.py ask_question.py --question "What is the content of this notebook? What topics are covered? Provide a complete overview briefly and concisely" --notebook-url "https://notebooklm.google.com/notebook/256b0760-a92f-4fd0-9d84-9a1cd0ace522"
pause

@echo off
chcp 65001 >nul
cd /d "%~dp0"
python scripts/run.py notebook_manager.py add --url "https://notebooklm.google.com/notebook/256b0760-a92f-4fd0-9d84-9a1cd0ace822" --name "工作总结" --description "工作总结笔记本" --topics "工作,总结"
pause

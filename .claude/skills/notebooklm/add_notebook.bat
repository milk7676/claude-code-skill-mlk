@echo off
chcp 65001 >nul
cd /d "%~dp0"
python scripts/run.py notebook_manager.py add --url "https://notebooklm.google.com/notebook/256b0760-a92f-4fd0-9d84-9a1cd0ace522"
pause

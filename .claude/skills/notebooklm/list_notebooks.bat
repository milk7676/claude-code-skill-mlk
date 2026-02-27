@echo off
chcp 65001 >nul
cd /d "%~dp0"
python scripts/run.py notebook_manager.py list
pause

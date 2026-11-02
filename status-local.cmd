@echo off
cd /d "%~dp0"
set PYTHONUTF8=1
start "Degron local - status" "%ComSpec%" /k ""%~dp0.venv\Scripts\python.exe" -u -I "%~dp0topics\degron-footprint\research\kaggle-roadmap-2026-10-31\local-runner.py" status"

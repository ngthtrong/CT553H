@echo off
cd /d "%~dp0"
set PYTHONUTF8=1
set PYTHONUNBUFFERED=1
start "Degron local CUDA - run" "%ComSpec%" /k ""%~dp0.venv\Scripts\python.exe" -u -I "%~dp0research\lora-refit-transfer-2026-11-16\session-entry.py" run %*"

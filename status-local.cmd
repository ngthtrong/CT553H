@echo off
cd /d "%~dp0"
set PYTHONUTF8=1
start "Degron local - status" "%ComSpec%" /k ""%~dp0.venv\Scripts\python.exe" -u -I "%~dp0research\lora-refit-transfer-2026-11-16\session-entry.py" status %*"

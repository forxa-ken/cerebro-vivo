@echo off
rem Abre la ventana para instalar Cerebro Vivo en un proyecto nuevo (spec 055)
cd /d "%~dp0"
if exist "venv\Scripts\pythonw.exe" (
    start "" "venv\Scripts\pythonw.exe" ".brain\biblioteca\kit-arranque\instalar_gui.py"
) else (
    start "" pythonw ".brain\biblioteca\kit-arranque\instalar_gui.py"
)

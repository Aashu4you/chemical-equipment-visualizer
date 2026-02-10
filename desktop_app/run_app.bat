@echo off
setlocal

REM Define the absolute path to Python (found from previous diagnostics)
SET SYSTEM_PYTHON="C:\Users\as421\AppData\Local\Programs\Python\Python313\python.exe"

REM Define the virtual environment path (relative to this script)
SET VENV_DIR=..\venv_new
SET VENV_PYTHON=%VENV_DIR%\Scripts\python.exe
SET VENV_PIP=%VENV_DIR%\Scripts\pip.exe

REM Check if the system python exists
if not exist %SYSTEM_PYTHON% (
    echo Error: System Python not found at %SYSTEM_PYTHON%
    echo Please install Python or update this script with the correct path.
    pause
    exit /b
)

REM Check if venv exists, if not create it
if not exist "%VENV_PYTHON%" (
    echo Creating virtual environment at %VENV_DIR%...
    %SYSTEM_PYTHON% -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo Failed to create virtual environment.
        pause
        exit /b
    )
)

REM Install dependencies
echo Installing dependencies...
"%VENV_PIP%" install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies.
    pause
    exit /b
)

REM Run the application
echo Starting Chemical Equipment Visualizer...
"%VENV_PYTHON%" main.py
if errorlevel 1 (
    echo Application crashed.
    pause
)
pause

@echo off
REM ImageConverter - Windows Launcher
REM Double-click this file to launch ImageConverter GUI

echo Starting ImageConverter...
echo.

REM Check if UV is installed
where uv >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: UV package manager not found!
    echo Please install UV first: https://github.com/astral-sh/uv
    echo.
    pause
    exit /b 1
)

REM Change to the directory where this batch file is located
cd /d "%~dp0"

REM Launch ImageConverter GUI using UV
uv run imageconverter

REM If the GUI closes with an error, show a pause
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ImageConverter exited with an error.
    pause
)

@echo off
REM IFC to Fragments Converter - Windows Batch Helper
REM Usage: ifc_convert.bat <source_dir> [target_dir] [options]

setlocal enabledelayedexpansion

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org/
    pause
    exit /b 1
)

REM Get the directory where this batch file is located
set CONVERTER_DIR=%~dp0

REM Build the command
set PYTHON_CMD=python "%CONVERTER_DIR%ifc_fragments_converter.py"

REM Add all arguments
:loop
if "%~1"=="" goto execute
set PYTHON_CMD=%PYTHON_CMD% "%~1"
shift
goto loop

:execute
echo.
echo ============================================================
echo   IFC TO FRAGMENTS CONVERTER - Windows Helper
echo ============================================================
echo.
echo Executing: %PYTHON_CMD%
echo.

REM Execute the Python script
%PYTHON_CMD%

REM Check result
if errorlevel 1 (
    echo.
    echo ============================================================
    echo ERROR: Conversion failed. Check the logs for details.
    echo ============================================================
    pause
    exit /b 1
) else (
    echo.
    echo ============================================================
    echo SUCCESS: Conversion completed successfully!
    echo ============================================================
    pause
    exit /b 0
)

@echo off
REM Activation script for the Python virtual environment

echo Activating Python virtual environment for IFC Converter...
call venv\Scripts\activate

echo.
echo Virtual environment activated!
echo Python executable: %VIRTUAL_ENV%\Scripts\python.exe
echo.
echo Available commands:
echo   python convert_ifc_to_fragments.py    - Run the IFC converter
echo   pip list                              - Show installed packages
echo   deactivate                            - Exit virtual environment
echo.
echo Directory structure:
echo   data\ifc\                             - Place IFC files here
echo   data\fragments\                       - Fragment files output here
echo   logs\                                 - Conversion logs
echo   reports\                              - JSON reports
echo.
echo To run the converter: python convert_ifc_to_fragments.py
echo.

cmd /k

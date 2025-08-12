@echo off
REM One-click IFC to Fragments converter
REM Place this in the XIFC directory and double-click to run

echo.
echo ============================================================
echo    🚀 IFC to Fragments Converter - One-Click Mode
echo ============================================================
echo.

cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo ❌ Virtual environment not found!
    echo    Please run setup first or use activate_venv.bat
    pause
    exit /b 1
)

REM Show current file counts
echo 📊 Current Status:
if exist "data\ifc" (
    for /f %%i in ('dir /b "data\ifc\*.ifc" 2^>nul ^| find /c /v ""') do set ifc_count=%%i
) else (
    set ifc_count=0
)

if exist "data\fragments" (
    for /f %%i in ('dir /b "data\fragments\*.frag" 2^>nul ^| find /c /v ""') do set frag_count=%%i
) else (
    set frag_count=0
)

echo    📥 IFC files found: %ifc_count%
echo    📤 Fragment files: %frag_count%
echo.

if %ifc_count%==0 (
    echo ⚠️  No IFC files found in data\ifc\
    echo    Please place your IFC files in the data\ifc\ directory first.
    echo.
    pause
    exit /b 0
)

echo 🔄 Starting conversion...
echo.

REM Run the converter
venv\Scripts\python.exe convert_ifc_to_fragments.py

echo.
echo ============================================================
echo 🎉 Conversion complete! Check data\fragments\ for results.
echo ============================================================
echo.
pause

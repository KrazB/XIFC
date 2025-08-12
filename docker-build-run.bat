@echo off
REM Docker Build and Run Script for XIFC - Windows
REM ===============================================

echo.
echo ============================================================
echo    🐳 XIFC Docker Setup for Windows
echo ============================================================
echo.

cd /d "%~dp0"

REM Check if Docker is running
docker version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running or not installed!
    echo.
    echo Please:
    echo 1. Install Docker Desktop from: https://www.docker.com/products/docker-desktop/
    echo 2. Start Docker Desktop
    echo 3. Wait for Docker to start completely
    echo 4. Run this script again
    echo.
    pause
    exit /b 1
)

echo ✅ Docker is running
echo.

REM Show current status
echo 📊 Current Status:
if exist "data\ifc" (
    for /f %%i in ('dir /b "data\ifc\*.ifc" 2^>nul ^| find /c /v ""') do set ifc_count=%%i
) else (
    set ifc_count=0
)

echo    📥 IFC files found: %ifc_count%
echo    📂 Data directory: %cd%\data
echo.

if %ifc_count%==0 (
    echo ⚠️  No IFC files found in data\ifc\
    echo    Please place your IFC files in the data\ifc\ directory first.
    echo.
    echo Example:
    echo    copy "C:\path\to\your\model.ifc" "data\ifc\"
    echo.
    set /p choice="Continue anyway? (y/N): "
    if /i not "%choice%"=="y" (
        echo Operation cancelled.
        pause
        exit /b 0
    )
)

echo 🔧 Building Docker image...
echo.
docker build -t xifc-converter .

if errorlevel 1 (
    echo.
    echo ❌ Docker build failed!
    echo Please check the error messages above.
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Docker image built successfully!
echo.

echo 🔄 Starting conversion...
echo.

REM Run the converter with Windows-specific volume mounting
docker run --rm -v "%cd%\data:/app/data" -v "%cd%\logs:/app/logs" -v "%cd%\reports:/app/reports" xifc-converter

if errorlevel 1 (
    echo.
    echo ❌ Conversion failed!
    echo Check the logs for details.
) else (
    echo.
    echo ✅ Conversion completed successfully!
    echo.
    echo 📤 Results available in: %cd%\data\fragments\
    echo 📊 Logs available in: %cd%\logs\
    echo 📈 Reports available in: %cd%\reports\
)

echo.
echo ============================================================
echo 🎉 Docker conversion complete!
echo ============================================================
echo.
pause

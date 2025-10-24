@echo off
echo ========================================
echo Building Pxgate for Windows
echo ========================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

echo.
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist Pxgate.spec del Pxgate.spec

echo.
echo Building executable...
pyinstaller ^
    --name=Pxgate ^
    --windowed ^
    --icon=app_icon.ico ^
    --add-data="resources;resources" ^
    --add-data="app_icon.ico;." ^
    --noconfirm ^
    --clean ^
    pxgate.py

if errorlevel 1 (
    echo.
    echo ❌ Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ Build completed successfully!
echo ========================================
echo.
echo Executable location: dist\Pxgate\Pxgate.exe
echo.
echo Creating distribution package...

REM Create distribution folder
if not exist "dist\Pxgate-Windows" mkdir "dist\Pxgate-Windows"
xcopy /E /I /Y "dist\Pxgate" "dist\Pxgate-Windows\Pxgate"

REM Create README for users
echo Pxgate - Professional Photo Culling Application > "dist\Pxgate-Windows\README.txt"
echo. >> "dist\Pxgate-Windows\README.txt"
echo To run: Double-click Pxgate.exe inside the Pxgate folder >> "dist\Pxgate-Windows\README.txt"
echo. >> "dist\Pxgate-Windows\README.txt"
echo Features: >> "dist\Pxgate-Windows\README.txt"
echo - Professional UI with enhanced typography and spacing >> "dist\Pxgate-Windows\README.txt"
echo - Dark mode with OLED optimization >> "dist\Pxgate-Windows\README.txt"
echo - Adaptive UI density for different workflows >> "dist\Pxgate-Windows\README.txt"
echo - Skeleton loading animations >> "dist\Pxgate-Windows\README.txt"
echo - RAW + JPG file support >> "dist\Pxgate-Windows\README.txt"
echo - Cross-platform photo sorting tool >> "dist\Pxgate-Windows\README.txt"

echo.
echo ========================================
echo 📦 Distribution package ready!
echo Location: dist\Pxgate-Windows\
echo ========================================
echo.
pause

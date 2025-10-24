@echo off
echo ========================================
echo Pxgate - Quick Build Script
echo Professional UI Enhanced Version
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo [1/5] Checking dependencies...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

pip show pillow >nul 2>&1
if errorlevel 1 (
    echo Installing Pillow...
    pip install pillow
)

pip show rawpy >nul 2>&1
if errorlevel 1 (
    echo Installing rawpy...
    pip install rawpy
)

pip show PyQt5 >nul 2>&1
if errorlevel 1 (
    echo Installing PyQt5...
    pip install PyQt5
)

echo.
echo [2/5] Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist Pxgate.spec del Pxgate.spec

echo.
echo [3/5] Building Windows executable...
echo This may take 2-5 minutes...
echo.

pyinstaller ^
    --onedir ^
    --windowed ^
    --icon=app_icon.ico ^
    --add-data="app_icon.ico;." ^
    --hidden-import=rawpy ^
    --hidden-import=imageio ^
    --hidden-import=PIL ^
    --collect-all rawpy ^
    --collect-all PySide6 ^
    --collect-all pillow_heif ^
    --hidden-import=PIL ^
    --hidden-import=PIL.Image ^
    --hidden-import=PIL.ExifTags ^
    --hidden-import=exifread ^
    --add-data="exiftool;exiftool" ^
    --noconfirm ^
    --clean ^
    pxgate.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo ❌ Build FAILED!
    echo ========================================
    echo.
    echo Check the error messages above.
    pause
    exit /b 1
)

echo.
echo [4/5] Creating distribution package...

REM Create distribution folder
if not exist "dist\Pxgate-Windows-v1.0" mkdir "dist\Pxgate-Windows-v1.0"
xcopy /E /I /Y "dist\Pxgate" "dist\Pxgate-Windows-v1.0\" 2>nul || true

REM Copy documentation
copy "DISTRIBUTION_README.md" "dist\Pxgate-Windows-v1.0\README.md" 2>nul
copy "START_HERE.md" "dist\Pxgate-Windows-v1.0\USER_GUIDE.md" 2>nul

REM Copy resources
if not exist "dist\Pxgate-Windows-v1.0\resources" mkdir "dist\Pxgate-Windows-v1.0\resources"
copy "resources\*" "dist\Pxgate-Windows-v1.0\resources\" 2>nul || true

REM Create quick start file
echo Pxgate - Professional Photo Culling > "dist\Pxgate-Windows-v1.0\QUICK_START.txt"
echo. >> "dist\Pxgate-Windows-v1.0\QUICK_START.txt"
echo 1. Double-click Pxgate.exe to run >> "dist\Pxgate-Windows-v1.0\QUICK_START.txt"
echo 2. Click "Load Images" to select a folder >> "dist\Pxgate-Windows-v1.0\QUICK_START.txt"
echo 3. Use WASD or arrow keys to navigate >> "dist\Pxgate-Windows-v1.0\QUICK_START.txt"
echo 4. Press 1-9 to move photos to folders >> "dist\Pxgate-Windows-v1.0\QUICK_START.txt"
echo. >> "dist\Pxgate-Windows-v1.0\QUICK_START.txt"
echo Professional UI Features: >> "dist\Pxgate-Windows-v1.0\QUICK_START.txt"
echo - Enhanced typography and spacing >> "dist\Pxgate-Windows-v1.0\QUICK_START.txt"
echo - Dark mode with OLED optimization >> "dist\Pxgate-Windows-v1.0\QUICK_START.txt"
echo - Adaptive UI density >> "dist\Pxgate-Windows-v1.0\QUICK_START.txt"
echo - Skeleton loading animations >> "dist\Pxgate-Windows-v1.0\QUICK_START.txt"

echo.
echo [5/5] Creating ZIP archive...
powershell Compress-Archive -Path "dist\Pxgate-Windows-v1.0" -DestinationPath "dist\Pxgate-Windows-v1.0.zip" -Force

echo.
echo ========================================
echo ✅ BUILD SUCCESSFUL!
echo ========================================
echo.
echo 📦 Distribution Package:
echo    dist\Pxgate-Windows-v1.0.zip
echo.
echo 📁 Folder:
echo    dist\Pxgate-Windows-v1.0\
echo.
echo 🚀 Executable:
echo    dist\build\build\build.exe
echo.
echo ========================================
echo.
echo You can now:
echo 1. Test: Run dist\Pxgate-Windows-v1.0\Pxgate.exe
echo 2. Distribute: Share dist\Pxgate-Windows-v1.0.zip
echo.
pause

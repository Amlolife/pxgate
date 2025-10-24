@echo off
echo ========================================
echo Pxgate - Fast Startup Build
echo Professional UI Enhanced Version
echo ========================================
echo.
echo This creates a FOLDER with fast startup
echo (Recommended for professional distribution)
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
echo [3/5] Building Windows application (FAST STARTUP MODE)...
echo This may take 2-5 minutes...
echo.

pyinstaller ^
    --name=Pxgate ^
    --windowed ^
    --onedir ^
    --icon=app_icon.ico ^
    --add-data="app_icon.ico;." ^
    --hidden-import=rawpy ^
    --hidden-import=imageio ^
    --hidden-import=PIL ^
    --collect-all rawpy ^
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
if not exist "dist\Pxgate-Windows-v1.0-Fast" mkdir "dist\Pxgate-Windows-v1.0-Fast"
xcopy /E /I /Y "dist\Pxgate" "dist\Pxgate-Windows-v1.0-Fast\Pxgate"

REM Copy documentation
copy "DISTRIBUTION_README.md" "dist\Pxgate-Windows-v1.0-Fast\README.md" 2>nul
copy "START_HERE.md" "dist\Pxgate-Windows-v1.0-Fast\USER_GUIDE.md" 2>nul

REM Create quick start file
echo Pxgate - Professional Photo Culling > "dist\Pxgate-Windows-v1.0-Fast\QUICK_START.txt"
echo. >> "dist\Pxgate-Windows-v1.0-Fast\QUICK_START.txt"
echo FAST STARTUP VERSION >> "dist\Pxgate-Windows-v1.0-Fast\QUICK_START.txt"
echo Opens in less than 1 second! >> "dist\Pxgate-Windows-v1.0-Fast\QUICK_START.txt"
echo. >> "dist\Pxgate-Windows-v1.0-Fast\QUICK_START.txt"
echo 1. Navigate to Pxgate folder >> "dist\Pxgate-Windows-v1.0-Fast\QUICK_START.txt"
echo 2. Double-click Pxgate.exe to run >> "dist\Pxgate-Windows-v1.0-Fast\QUICK_START.txt"
echo 3. Click "Load Images" to select a folder >> "dist\Pxgate-Windows-v1.0-Fast\QUICK_START.txt"
echo 4. Use WASD or arrow keys to navigate >> "dist\Pxgate-Windows-v1.0-Fast\QUICK_START.txt"
echo 5. Press 1-9 to move photos to folders >> "dist\Pxgate-Windows-v1.0-Fast\QUICK_START.txt"
echo. >> "dist\Pxgate-Windows-v1.0-Fast\QUICK_START.txt"
echo Professional UI Features: >> "dist\Pxgate-Windows-v1.0-Fast\QUICK_START.txt"
echo - Enhanced typography and spacing >> "dist\Pxgate-Windows-v1.0-Fast\QUICK_START.txt"
echo - Dark mode with OLED optimization >> "dist\Pxgate-Windows-v1.0-Fast\QUICK_START.txt"
echo - Adaptive UI density >> "dist\Pxgate-Windows-v1.0-Fast\QUICK_START.txt"
echo - Skeleton loading animations >> "dist\Pxgate-Windows-v1.0-Fast\QUICK_START.txt"
echo - INSTANT STARTUP (less than 1 second!) >> "dist\Pxgate-Windows-v1.0-Fast\QUICK_START.txt"

echo.
echo [5/5] Creating ZIP archive...
powershell Compress-Archive -Path "dist\Pxgate-Windows-v1.0-Fast" -DestinationPath "dist\Pxgate-Windows-v1.0-Fast.zip" -Force

echo.
echo ========================================
echo ✅ BUILD SUCCESSFUL!
echo ========================================
echo.
echo ⚡ FAST STARTUP VERSION
echo    Opens in less than 1 second!
echo.
echo 📦 Distribution Package:
echo    dist\Pxgate-Windows-v1.0-Fast.zip
echo.
echo 📁 Folder Structure:
echo    dist\Pxgate-Windows-v1.0-Fast\
echo    └── Pxgate\
echo        ├── Pxgate.exe (Main executable)
echo        ├── *.dll (Required libraries)
echo        └── _internal\ (Dependencies)
echo.
echo 🚀 Executable:
echo    dist\Pxgate-Windows-v1.0-Fast\Pxgate\Pxgate.exe
echo.
echo ========================================
echo.
echo COMPARISON:
echo.
echo Single EXE (BUILD_NOW.bat):
echo   + Single file
echo   - Slower startup (3-8 seconds)
echo   - Larger size (~150 MB)
echo.
echo Folder (BUILD_FAST.bat - THIS):
echo   + INSTANT startup (less than 1 second)
echo   + Smaller size (~80-100 MB total)
echo   - Multiple files (but in one folder)
echo.
echo RECOMMENDED: Use this fast version!
echo Professional apps use folder distribution.
echo.
pause

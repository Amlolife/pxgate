#!/bin/bash

# Ensure Python 3.12 is in PATH
export PATH="/Library/Frameworks/Python.framework/Versions/3.12/bin:$PATH"

echo "========================================"
echo "Pxgate - Quick Build Script for macOS"
echo "Professional UI Enhanced Version"
echo "========================================"
echo

# Check Python
python3 --version > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "ERROR: Python3 not found!"
    echo "Please install Python 3.8+ first."
    exit 1
fi

echo "[1/5] Checking dependencies..."
python3 -m pip show pyinstaller > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Installing PyInstaller..."
    python3 -m pip install pyinstaller
fi

python3 -m pip show pillow > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Installing Pillow..."
    python3 -m pip install pillow
fi

python3 -m pip show rawpy > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Installing rawpy..."
    python3 -m pip install rawpy
fi

python3 -m pip show pyside6 > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Installing PySide6..."
    python3 -m pip install pyside6
fi

# Additional dependencies from code
python3 -m pip show numpy > /dev/null 2>&1 || python3 -m pip install numpy
python3 -m pip show piexif > /dev/null 2>&1 || python3 -m pip install piexif
python3 -m pip show psutil > /dev/null 2>&1 || python3 -m pip install psutil
python3 -m pip show pillow-heif > /dev/null 2>&1 || python3 -m pip install pillow-heif

echo
echo "[2/5] Cleaning previous builds..."
rm -rf build dist Pxgate.spec

echo
echo "[3/5] Building macOS application..."
echo "This may take 2-5 minutes..."
echo

# Assuming app_icon.icns exists; if not, you may need to create it from .ico or .iconset
/Library/Frameworks/Python.framework/Versions/3.12/bin/pyinstaller \
    --name=Pxgate \
    --windowed \
    --onedir \
    --icon=app_icon.icns \
    --hidden-import=rawpy \
    --hidden-import=imageio \
    --hidden-import=PIL \
    --hidden-import=numpy \
    --hidden-import=piexif \
    --hidden-import=psutil \
    --hidden-import=pillow_heif \
    --collect-all rawpy \
    --noconfirm \
    --clean \
    pxgate.py

if [ $? -ne 0 ]; then
    echo
    echo "========================================"
    echo "❌ Build FAILED!"
    echo "========================================"
    echo
    echo "Check the error messages above."
    exit 1
fi

echo
echo "[4/5] Creating distribution package..."

# Create distribution folder
mkdir -p "dist/Pxgate-macOS-v1.0"
cp -r "dist/Pxgate.app" "dist/Pxgate-macOS-v1.0/"

# Copy documentation
cp "DISTRIBUTION_README.md" "dist/Pxgate-macOS-v1.0/README.md" 2>/dev/null || true
cp "START_HERE.md" "dist/Pxgate-macOS-v1.0/USER_GUIDE.md" 2>/dev/null || true

# Create quick start file
cat > "dist/Pxgate-macOS-v1.0/QUICK_START.txt" << EOF
Pxgate - Professional Photo Culling

1. Double-click Pxgate.app to run
2. Click "Load Images" to select a folder
3. Use WASD or arrow keys to navigate
4. Press 1-9 to move photos to folders

Professional UI Features:
- Enhanced typography and spacing
- Dark mode with OLED optimization
- Adaptive UI density
- Skeleton loading animations
EOF

echo
echo "[5/5] Creating ZIP archive..."
cd dist
zip -r "Pxgate-macOS-v1.0.zip" "Pxgate-macOS-v1.0"
cd ..

echo
echo "========================================"
echo "✅ BUILD SUCCESSFUL!"
echo "========================================"
echo
echo "📦 Distribution Package:"
echo "   dist/Pxgate-macOS-v1.0.zip"
echo
echo "📁 Folder:"
echo "   dist/Pxgate-macOS-v1.0/"
echo
echo "🚀 Application:"
echo "   dist/Pxgate-macOS-v1.0/Pxgate.app"
echo
echo "========================================"
echo
echo "You can now:"
echo "1. Test: Open dist/Pxgate-macOS-v1.0/Pxgate.app"
echo "2. Distribute: Share dist/Pxgate-macOS-v1.0.zip"
echo

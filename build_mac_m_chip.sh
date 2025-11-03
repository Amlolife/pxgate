#!/bin/bash

echo "========================================"
echo "Building Pxgate for Apple Silicon (M-Chip)"
echo "========================================"
echo ""

# Verify we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Error: This script must be run on macOS"
    exit 1
fi

# Check architecture
ARCH=$(uname -m)
echo "Detected architecture: $ARCH"

if [[ "$ARCH" != "arm64" ]]; then
    echo "⚠️  Warning: Not running on Apple Silicon (ARM64)"
    echo "   Current architecture: $ARCH"
    echo "   This build will be for Intel/Rosetta 2"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✓ Running on Apple Silicon - native ARM64 build"
fi

echo ""

# Check Python architecture
PYTHON_ARCH=$(python3 -c "import platform; print(platform.machine())")
echo "Python architecture: $PYTHON_ARCH"

if [[ "$ARCH" == "arm64" ]] && [[ "$PYTHON_ARCH" != "arm64" ]]; then
    echo "⚠️  Warning: Python is not ARM64 native!"
    echo "   You're using an Intel Python on an M-chip Mac"
    echo "   This will create an Intel build that runs via Rosetta 2"
    echo ""
    echo "To install ARM64 Python:"
    echo "  brew install python@3.11"
    echo "  or download from python.org"
    echo ""
    read -p "Continue with Intel Python? (y/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""

# Check if required packages are installed
echo "Checking dependencies..."

python3 -c "import PyInstaller" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing PyInstaller..."
    pip3 install pyinstaller
fi

python3 -c "import PySide6" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ PySide6 not found. Installing dependencies..."
    pip3 install -r requirements.txt
fi

# Verify critical M-chip compatible packages
echo ""
echo "Verifying M-chip compatible packages..."

PACKAGES=("numpy" "PySide6" "rawpy" "Pillow" "pillow_heif")
for pkg in "${PACKAGES[@]}"; do
    python3 -c "import $pkg; print('✓ $pkg')" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "❌ $pkg not installed"
        exit 1
    fi
done

echo ""
echo "All dependencies verified!"

# Create .icns file if needed
if [ ! -f "app_icon.icns" ]; then
    echo ""
    echo "Creating macOS icon (.icns)..."
    if [ -d "app_icon.iconset" ]; then
        iconutil -c icns app_icon.iconset
        if [ $? -eq 0 ]; then
            echo "✓ app_icon.icns created"
        else
            echo "⚠️  Failed to create .icns, continuing without icon"
        fi
    else
        echo "⚠️  app_icon.iconset not found, continuing without icon"
    fi
fi

echo ""
echo "Cleaning previous builds..."
rm -rf build dist/*.app

echo ""
echo "Building application with PyInstaller..."
echo "Using spec file: pxgate-mac.spec"
echo ""

pyinstaller pxgate-mac.spec

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Build failed!"
    exit 1
fi

echo ""
echo "========================================"
echo "✅ Build completed successfully!"
echo "========================================"

# Verify the build architecture
if [ -f "dist/Pxgate.app/Contents/MacOS/Pxgate" ]; then
    echo ""
    echo "Verifying build architecture..."
    BUILD_ARCH=$(file dist/Pxgate.app/Contents/MacOS/Pxgate | grep -o "arm64\|x86_64")
    
    if [[ "$BUILD_ARCH" == "arm64" ]]; then
        echo "✓ Native ARM64 build (Apple Silicon optimized)"
    elif [[ "$BUILD_ARCH" == "x86_64" ]]; then
        echo "⚠️  Intel x86_64 build (will run via Rosetta 2 on M-chip)"
    else
        echo "⚠️  Could not determine architecture"
    fi
fi

echo ""
echo "Application location: dist/Pxgate.app"
echo ""

# Test if app can launch
echo "Testing if app can launch..."
open -a "dist/Pxgate.app" --args --test 2>/dev/null &
APP_PID=$!
sleep 2

if ps -p $APP_PID > /dev/null 2>&1; then
    echo "✓ App launched successfully"
    kill $APP_PID 2>/dev/null
else
    echo "⚠️  App may have issues launching (check logs)"
fi

echo ""
echo "========================================"
echo "Next steps:"
echo "========================================"
echo ""
echo "1. Test the app:"
echo "   open dist/Pxgate.app"
echo ""
echo "2. Create distribution package:"
echo "   mkdir -p dist/Pxgate-macOS-M-Chip"
echo "   cp -R dist/Pxgate.app dist/Pxgate-macOS-M-Chip/"
echo ""
echo "3. Create DMG installer:"
echo "   hdiutil create -volname Pxgate -srcfolder dist/Pxgate-macOS-M-Chip -ov -format UDZO dist/Pxgate-M-Chip.dmg"
echo ""
echo "4. Check logs if issues occur:"
echo "   ~/Library/Application Support/Pxgate/logs/"
echo ""

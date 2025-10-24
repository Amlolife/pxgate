#!/bin/bash

echo "========================================"
echo "Building Pxgate for macOS"
echo "========================================"
echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠️  Warning: This script should be run on macOS"
    echo "   You can still prepare files, but the .app bundle"
    echo "   should be built on a Mac."
    echo ""
fi

# Check if PyInstaller is installed
python3 -c "import PyInstaller" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing PyInstaller..."
    pip3 install pyinstaller
fi

# Create .icns file if it doesn't exist
if [ ! -f "app_icon.icns" ]; then
    echo ""
    echo "Creating macOS icon (.icns)..."
    if [ -d "app_icon.iconset" ]; then
        iconutil -c icns app_icon.iconset
        if [ $? -eq 0 ]; then
            echo "✓ app_icon.icns created successfully"
        else
            echo "❌ Failed to create .icns file"
            echo "   Make sure you're running this on macOS"
            exit 1
        fi
    else
        echo "❌ app_icon.iconset folder not found!"
        echo "   Run create_mac_icon.py first"
        exit 1
    fi
fi

echo ""
echo "Cleaning previous builds..."
rm -rf build dist Pxgate.spec

echo ""
echo "Building application bundle..."
pyinstaller \
    --name=Pxgate \
    --windowed \
    --icon=app_icon.icns \
    --add-data="resources:resources" \
    --add-data="app_icon.icns:." \
    --noconfirm \
    --clean \
    --osx-bundle-identifier=com.pxgate.app \
    pxgate.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Build failed!"
    exit 1
fi

echo ""
echo "========================================"
echo "✅ Build completed successfully!"
echo "========================================"
echo ""
echo "Application location: dist/Pxgate.app"
echo ""
echo "Creating distribution package..."

# Create distribution folder
mkdir -p "dist/Pxgate-macOS"
cp -R "dist/Pxgate.app" "dist/Pxgate-macOS/"

# Create README for users
cat > "dist/Pxgate-macOS/README.txt" << EOF
Pxgate - Photo Culling Application

To install:
1. Drag Pxgate.app to your Applications folder
2. Double-click to run

Note: On first launch, you may need to right-click and select "Open"
to bypass macOS Gatekeeper (for unsigned apps).

Modern UI with PX branding
Cross-platform photo sorting tool
EOF

echo ""
echo "========================================"
echo "📦 Distribution package ready!"
echo "Location: dist/Pxgate-macOS/"
echo "========================================"
echo ""
echo "To create a DMG installer, run:"
echo "  hdiutil create -volname Pxgate -srcfolder dist/Pxgate-macOS -ov -format UDZO dist/Pxgate-macOS.dmg"
echo ""

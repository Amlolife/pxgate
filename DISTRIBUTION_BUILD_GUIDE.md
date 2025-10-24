# 📦 Distribution Build Guide - Pxgate

Complete guide to building distributable packages for **Windows** and **macOS**.

---

## 📋 Prerequisites

### Required Tools:
```bash
pip install pyinstaller pillow rawpy imageio numpy
```

### Platform-Specific:
- **Windows**: Windows 10/11, Python 3.8+
- **macOS**: macOS 10.14+, Python 3.8+, Xcode Command Line Tools

---

## 🚀 Quick Build Commands

### **Windows (One-Line Build)**
```bash
pyinstaller --name="Pxgate" --windowed --onefile --icon=icon.ico --add-data "icon.ico;." --hidden-import=rawpy --hidden-import=imageio --hidden-import=PIL --collect-all rawpy VibeCulling.py
```

### **macOS (One-Line Build)**
```bash
pyinstaller --name="Pxgate" --windowed --onefile --icon=icon.icns --add-data "icon.icns:." --hidden-import=rawpy --hidden-import=imageio --hidden-import=PIL --collect-all rawpy VibeCulling.py
```

---

## 📝 PyInstaller Spec File (Advanced)

Save this as `pxgate.spec` in your project directory:

```python
# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# Collect all rawpy dependencies
rawpy_datas, rawpy_binaries, rawpy_hiddenimports = collect_all('rawpy')

a = Analysis(
    ['VibeCulling.py'],
    pathex=[],
    binaries=rawpy_binaries,
    datas=[
        ('icon.ico', '.') if sys.platform == 'win32' else ('icon.icns', '.'),
    ] + rawpy_datas,
    hiddenimports=[
        'rawpy',
        'imageio',
        'PIL',
        'PIL.Image',
        'PIL.ImageQt',
        'numpy',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
    ] + rawpy_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'pandas',
        'tkinter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Pxgate',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if sys.platform == 'win32' else 'icon.icns',
)

# macOS App Bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='Pxgate.app',
        icon='icon.icns',
        bundle_identifier='com.pxgate.app',
        info_plist={
            'CFBundleName': 'Pxgate',
            'CFBundleDisplayName': 'Pxgate',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleVersion': '1.0.0',
            'NSHighResolutionCapable': 'True',
            'LSMinimumSystemVersion': '10.14.0',
            'NSRequiresAquaSystemAppearance': 'False',
        },
    )
```

---

## 🔨 Build Scripts

### **Windows Build Script** (`build_windows.bat`)

```batch
@echo off
echo ========================================
echo Building Pxgate for Windows
echo ========================================

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build with PyInstaller
pyinstaller pxgate.spec

REM Check if build succeeded
if exist "dist\Pxgate.exe" (
    echo.
    echo ========================================
    echo Build successful!
    echo Executable: dist\Pxgate.exe
    echo ========================================
    
    REM Optional: Create distribution folder
    if not exist "dist_release" mkdir dist_release
    copy "dist\Pxgate.exe" "dist_release\"
    copy "README.md" "dist_release\" 2>nul
    copy "LICENSE" "dist_release\" 2>nul
    
    echo.
    echo Distribution folder created: dist_release\
) else (
    echo.
    echo ========================================
    echo Build failed!
    echo ========================================
    exit /b 1
)

pause
```

### **macOS Build Script** (`build_macos.sh`)

```bash
#!/bin/bash

echo "========================================"
echo "Building Pxgate for macOS"
echo "========================================"

# Clean previous builds
rm -rf build dist

# Build with PyInstaller
pyinstaller pxgate.spec

# Check if build succeeded
if [ -d "dist/Pxgate.app" ]; then
    echo ""
    echo "========================================"
    echo "Build successful!"
    echo "Application: dist/Pxgate.app"
    echo "========================================"
    
    # Optional: Create DMG
    echo ""
    echo "Creating DMG..."
    hdiutil create -volname "Pxgate" -srcfolder "dist/Pxgate.app" -ov -format UDZO "dist/Pxgate.dmg"
    
    if [ -f "dist/Pxgate.dmg" ]; then
        echo "DMG created: dist/Pxgate.dmg"
    fi
    
    # Optional: Code signing (requires Apple Developer account)
    # codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" "dist/Pxgate.app"
    # codesign --verify --verbose "dist/Pxgate.app"
    
else
    echo ""
    echo "========================================"
    echo "Build failed!"
    echo "========================================"
    exit 1
fi
```

Make executable:
```bash
chmod +x build_macos.sh
```

---

## 🎨 Icon Files

### **Windows Icon** (`icon.ico`)
- Format: ICO
- Sizes: 16x16, 32x32, 48x48, 256x256
- Tool: Use online converter or Photoshop

### **macOS Icon** (`icon.icns`)
- Format: ICNS
- Sizes: 16x16 to 1024x1024
- Tool: Use `iconutil` or online converter

**Quick Icon Creation:**
```bash
# macOS - Create iconset
mkdir icon.iconset
# Add icon files: icon_16x16.png, icon_32x32.png, etc.
iconutil -c icns icon.iconset -o icon.icns

# Windows - Use online tool or ImageMagick
convert icon.png -define icon:auto-resize=256,128,64,48,32,16 icon.ico
```

---

## 📦 Distribution Checklist

### **Before Building:**
- [ ] Update version number in code
- [ ] Test application thoroughly
- [ ] Prepare icon files (icon.ico, icon.icns)
- [ ] Update README.md
- [ ] Update LICENSE file
- [ ] Clean up debug code and logging

### **Windows Distribution:**
- [ ] Build executable
- [ ] Test on clean Windows machine
- [ ] Create installer (optional - use Inno Setup)
- [ ] Sign executable (optional - requires code signing certificate)
- [ ] Create ZIP archive
- [ ] Test installation

### **macOS Distribution:**
- [ ] Build .app bundle
- [ ] Test on clean macOS machine
- [ ] Create DMG
- [ ] Sign app (optional - requires Apple Developer account)
- [ ] Notarize app (optional - for Gatekeeper)
- [ ] Test installation

---

## 🔧 Troubleshooting

### **Issue: "Module not found" errors**
**Solution**: Add missing modules to `hiddenimports` in spec file

### **Issue: RAW file support not working**
**Solution**: Ensure `--collect-all rawpy` is included

### **Issue: Large executable size**
**Solution**: 
- Use `--exclude-module` for unused libraries
- Consider using `--onedir` instead of `--onefile`

### **Issue: macOS "App is damaged" error**
**Solution**: 
```bash
xattr -cr dist/Pxgate.app
```

### **Issue: Windows antivirus flags executable**
**Solution**: 
- Code sign the executable
- Submit to antivirus vendors for whitelisting
- Use UPX compression: `--upx-dir=/path/to/upx`

---

## 📊 Build Size Optimization

### **Reduce Size:**
```python
# In spec file, exclude unused modules
excludes=[
    'matplotlib',
    'scipy',
    'pandas',
    'tkinter',
    'unittest',
    'test',
    'distutils',
]
```

### **Expected Sizes:**
- **Windows**: ~80-150 MB (with RAW support)
- **macOS**: ~100-180 MB (with RAW support)

---

## 🚢 Advanced: Creating Installers

### **Windows Installer (Inno Setup)**

Create `installer.iss`:
```inno
[Setup]
AppName=Pxgate
AppVersion=1.0.0
DefaultDirName={pf}\Pxgate
DefaultGroupName=Pxgate
OutputDir=dist_installer
OutputBaseFilename=Pxgate_Setup
Compression=lzma2
SolidCompression=yes

[Files]
Source: "dist\Pxgate.exe"; DestDir: "{app}"
Source: "README.md"; DestDir: "{app}"; Flags: isreadme

[Icons]
Name: "{group}\Pxgate"; Filename: "{app}\Pxgate.exe"
Name: "{commondesktop}\Pxgate"; Filename: "{app}\Pxgate.exe"

[Run]
Filename: "{app}\Pxgate.exe"; Description: "Launch Pxgate"; Flags: postinstall nowait skipifsilent
```

Build:
```bash
iscc installer.iss
```

### **macOS DMG (Advanced)**

Create custom DMG with background image:
```bash
# Create DMG with custom settings
create-dmg \
  --volname "Pxgate" \
  --volicon "icon.icns" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "Pxgate.app" 200 190 \
  --hide-extension "Pxgate.app" \
  --app-drop-link 600 185 \
  "dist/Pxgate.dmg" \
  "dist/Pxgate.app"
```

---

## ✅ Final Steps

### **1. Test Distribution**
- Install on clean machine
- Test all features
- Check file associations
- Verify icon displays correctly

### **2. Create Release Package**
```
Pxgate_v1.0.0_Windows.zip
├── Pxgate.exe
├── README.md
└── LICENSE

Pxgate_v1.0.0_macOS.dmg
└── Pxgate.app
```

### **3. Upload to Distribution Platform**
- GitHub Releases
- Your website
- App stores (requires additional setup)

---

## 📝 Version Management

Update version in multiple places:
1. `VibeCulling.py` - App title/about dialog
2. `pxgate.spec` - CFBundleVersion (macOS)
3. `installer.iss` - AppVersion (Windows)
4. `README.md` - Version number

---

## 🎯 Quick Reference

| Task | Windows Command | macOS Command |
|------|----------------|---------------|
| **Build** | `pyinstaller pxgate.spec` | `pyinstaller pxgate.spec` |
| **Clean** | `rmdir /s build dist` | `rm -rf build dist` |
| **Test** | `dist\Pxgate.exe` | `open dist/Pxgate.app` |
| **Package** | Create ZIP | Create DMG |

---

**Ready to build!** Follow the steps above to create professional distributions for both platforms. 🚀

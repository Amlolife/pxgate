# 📦 Pxgate - Build & Distribution Guide

## Quick Start

### **Windows** 🪟
```bash
# Simply run:
build_windows.bat

# Output: dist/Pxgate-Windows/
```

### **macOS** 🍎
```bash
# Make script executable:
chmod +x build_macos.sh

# Run:
./build_macos.sh

# Output: dist/Pxgate-macOS/
```

---

## Prerequisites

### Both Platforms
- Python 3.8 or higher
- All dependencies installed: `pip install -r requirements.txt`
- PyInstaller (auto-installed by build scripts)

### macOS Only
- Xcode Command Line Tools (for `iconutil`)
- Run on an actual Mac to create the .app bundle

---

## Detailed Build Process

### Windows Build

1. **Prepare**
   ```bash
   pip install -r requirements.txt
   ```

2. **Build**
   ```bash
   build_windows.bat
   ```

3. **Output**
   - `dist/Pxgate-Windows/Pxgate/Pxgate.exe` - Main executable
   - All dependencies bundled
   - Ready to distribute as a ZIP file

4. **Distribute**
   - Compress `dist/Pxgate-Windows/` to `Pxgate-Windows.zip`
   - Users extract and run `Pxgate.exe`

### macOS Build

1. **Prepare** (on Mac)
   ```bash
   pip3 install -r requirements.txt
   python3 create_mac_icon.py  # If not done already
   ```

2. **Build**
   ```bash
   chmod +x build_macos.sh
   ./build_macos.sh
   ```

3. **Output**
   - `dist/Pxgate-macOS/Pxgate.app` - Application bundle
   - Ready to drag to Applications folder

4. **Create DMG (Optional)**
   ```bash
   hdiutil create -volname Pxgate -srcfolder dist/Pxgate-macOS -ov -format UDZO dist/Pxgate-macOS.dmg
   ```

5. **Distribute**
   - Share the DMG file or ZIP the .app
   - Users drag to Applications folder

---

## File Structure After Build

### Windows
```
dist/Pxgate-Windows/
├── Pxgate/
│   ├── Pxgate.exe          ← Main executable
│   ├── resources/          ← App resources
│   ├── app_icon.ico
│   └── [Python libraries]
└── README.txt
```

### macOS
```
dist/Pxgate-macOS/
├── Pxgate.app              ← Application bundle
│   └── Contents/
│       ├── MacOS/
│       │   └── Pxgate      ← Executable
│       ├── Resources/
│       │   ├── app_icon.icns
│       │   └── resources/
│       └── Info.plist
└── README.txt
```

---

## Code Signing (Optional but Recommended)

### Windows
```bash
# Using SignTool (requires certificate)
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com dist/Pxgate-Windows/Pxgate/Pxgate.exe
```

### macOS
```bash
# Sign the app (requires Apple Developer account)
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" dist/Pxgate-macOS/Pxgate.app

# Notarize (for macOS 10.15+)
xcrun notarytool submit dist/Pxgate-macOS.dmg --apple-id your@email.com --team-id TEAMID --password app-specific-password
```

---

## Testing Builds

### Windows
1. Navigate to `dist/Pxgate-Windows/Pxgate/`
2. Double-click `Pxgate.exe`
3. Verify:
   - App launches with PX icon
   - Modern blue UI appears
   - All features work

### macOS
1. Open `dist/Pxgate-macOS/`
2. Double-click `Pxgate.app`
3. If blocked by Gatekeeper:
   - Right-click → Open
   - Click "Open" in dialog
4. Verify same as Windows

---

## Distribution Checklist

- [ ] Build on Windows machine → `Pxgate-Windows.zip`
- [ ] Build on Mac machine → `Pxgate-macOS.dmg` or `.zip`
- [ ] Test both builds on clean machines
- [ ] Create release notes
- [ ] Upload to distribution platform (GitHub, website, etc.)
- [ ] (Optional) Code sign for better user experience

---

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### macOS: "iconutil not found"
Install Xcode Command Line Tools:
```bash
xcode-select --install
```

### Windows: Build script won't run
Run as Administrator or check antivirus settings

### Large file size
This is normal - PyInstaller bundles Python and all dependencies (~100-200MB)

---

## Version Updates

Update version in:
1. `version.txt` - App version number
2. Build scripts - Update any version references
3. README files - Update version in documentation

---

## Support

For build issues:
1. Check Python version: `python --version` (3.8+)
2. Verify dependencies: `pip list`
3. Check build logs in console output
4. Ensure all resource files are present

---

## What's Included

✅ Modern PX logo (blue rounded square)
✅ Cross-platform icon files (.ico and .icns)
✅ Automated build scripts
✅ Modern UI with blue accent theme
✅ All dependencies bundled
✅ Single-file distribution ready
✅ User-friendly README files

Ready to distribute! 🚀

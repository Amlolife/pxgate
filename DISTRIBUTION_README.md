# 📦 Pxgate - Distribution Package

**Professional Photo Culling Application with Enhanced UI**

Version: 1.0.0  
Platform: Windows & macOS

---

## ✨ What's New in This Version

### **Professional UI Enhancements**
- ✅ **Enhanced Typography** - Clear visual hierarchy with professional font system
- ✅ **Improved Spacing** - Comfortable, breathable layout (50% more spacing)
- ✅ **Consistent Design** - Professional border radius and spacing systems
- ✅ **Dark Mode Variants** - Standard, True Black (OLED), and Dim modes
- ✅ **Skeleton Loading** - Smooth loading animations for thumbnails
- ✅ **Adaptive Density** - UI automatically adjusts based on image count
- ✅ **Semantic Colors** - Color-coded actions for better UX

### **Core Features**
- Fast photo culling workflow
- RAW + JPG file support
- Keyboard-driven navigation
- Grid and single-image views
- Undo/Redo support
- Session management
- Multi-folder sorting

---

## 🚀 Quick Start

### **Windows**
1. Extract `Pxgate-Windows.zip`
2. Navigate to `Pxgate` folder
3. Double-click `Pxgate.exe`

### **macOS**
1. Open `Pxgate.dmg`
2. Drag `Pxgate.app` to Applications folder
3. Double-click to run

**First Time on macOS**: Right-click → Open (to bypass Gatekeeper)

---

## 📋 System Requirements

### **Windows**
- Windows 10 or later (64-bit)
- 4 GB RAM minimum (8 GB recommended)
- 500 MB free disk space
- Display: 1920x1080 or higher recommended

### **macOS**
- macOS 10.14 (Mojave) or later
- 4 GB RAM minimum (8 GB recommended)
- 500 MB free disk space
- Display: 1920x1080 or higher recommended

---

## 🎯 Key Features

### **Professional Workflow**
- **Fast Navigation**: WASD or arrow keys
- **Quick Sorting**: Number keys (1-9) to move photos
- **Batch Operations**: Grid mode with multi-select
- **Undo/Redo**: Ctrl+Z / Ctrl+Y (Cmd on Mac)

### **Image Support**
- **JPG/JPEG**: Full support
- **RAW Formats**: ARW, CR2, CR3, NEF, DNG, RAF, and more
- **Linked Files**: Automatically handle JPG+RAW pairs

### **View Modes**
- **Fit**: Scale to window
- **100%**: Pixel-perfect view
- **Custom Zoom**: 10% to 500%
- **Grid Mode**: Overview with thumbnails
- **Compare Mode**: Side-by-side A/B comparison

### **Professional UI**
- **Adaptive Density**: UI adjusts for 10 or 10,000 images
- **OLED Dark Mode**: Pure black for OLED screens
- **Skeleton Loading**: Professional loading states
- **Typography Hierarchy**: Clear visual organization

---

## ⌨️ Keyboard Shortcuts

### **Navigation**
- `W/A/S/D` or `Arrow Keys` - Navigate photos
- `Enter` - View photo list
- `F5` - Refresh folder

### **View**
- `F1/F2/F3` - Zoom modes (Fit/100%/Custom)
- `Space` - Toggle zoom
- `ESC` - Zoom out or exit grid
- `Z/X` - Zoom out/in (custom mode)
- `G` - Toggle grid mode
- `C` - Toggle compare mode
- `Q/E` - Rotate image

### **File Operations**
- `1-9` - Move to folder 1-9
- `Shift + 1-9` - Copy to folder 1-9
- `Ctrl+Z` - Undo move
- `Ctrl+Y` - Redo move
- `Delete` - Reset state

### **Grid Mode**
- `Ctrl+A` - Select all
- `Shift+A/D` - Previous/Next page

---

## 📁 Folder Structure

```
Pxgate/
├── Pxgate.exe (Windows) or Pxgate.app (macOS)
├── README.txt
└── [Application files]
```

**User Data**: Stored in application directory
- `pxgate_data.json` - Session state
- `logs/` - Application logs (if enabled)

---

## 🎨 UI Customization

### **Dark Mode Variants**
The app includes three dark mode options:
1. **Standard Dark** - Balanced for all displays
2. **True Black** - OLED optimized (pure #000000)
3. **Dim Mode** - Reduced brightness for night work

*Currently requires code modification to switch. UI toggle coming in future update.*

### **Adaptive Density**
UI automatically adjusts spacing based on image count:
- **<100 images**: Luxurious spacing
- **100-500**: Normal spacing
- **500-1000**: Compact spacing
- **>1000**: Ultra-compact spacing

---

## 🔧 Troubleshooting

### **Windows**

**Issue**: "Windows protected your PC" warning  
**Solution**: Click "More info" → "Run anyway"

**Issue**: Antivirus blocks the app  
**Solution**: Add exception for Pxgate.exe

**Issue**: App doesn't start  
**Solution**: Install Visual C++ Redistributable 2015-2022

### **macOS**

**Issue**: "App can't be opened because it is from an unidentified developer"  
**Solution**: Right-click app → Open → Open

**Issue**: "App is damaged and can't be opened"  
**Solution**: Run in Terminal:
```bash
xattr -cr /Applications/Pxgate.app
```

**Issue**: RAW files not loading  
**Solution**: Ensure you have sufficient permissions for the folder

### **General**

**Issue**: Slow performance with large collections  
**Solution**: 
- Use grid mode for overview
- Enable adaptive density (automatic)
- Close other applications

**Issue**: High memory usage  
**Solution**:
- App automatically manages memory
- Restart app if memory exceeds 2GB

---

## 📊 Performance Tips

### **For Best Performance**:
1. **Use SSD** - Faster image loading
2. **16GB RAM** - Smooth with large collections
3. **Dedicated GPU** - Better zoom/pan performance
4. **Close Background Apps** - More resources for Pxgate

### **Optimizing Workflow**:
1. **Grid Mode First** - Quick overview of all photos
2. **Keyboard Navigation** - Faster than mouse
3. **Batch Operations** - Select multiple in grid
4. **Session Save** - Resume work anytime

---

## 🆘 Support

### **Documentation**
- Full user guide: See `START_HERE.md` in source
- Keyboard shortcuts: Press `?` in app (if implemented)

### **Known Issues**
- Very large RAW files (>100MB) may load slowly
- Grid mode with 10,000+ images may have slight lag
- Some exotic RAW formats may not be supported

### **Reporting Bugs**
Please include:
1. Operating system and version
2. Steps to reproduce
3. Screenshot if applicable
4. Log file (if available)

---

## 📜 License

See LICENSE file for details.

---

## 🙏 Credits

**Pxgate** - Professional Photo Culling Tool

Built with:
- Python
- PyQt5
- Pillow
- rawpy
- imageio

Professional UI enhancements implemented October 2025.

---

## 🔄 Updates

**Version 1.0.0** (Current)
- Professional UI enhancements
- Improved spacing and typography
- Dark mode variants
- Skeleton loading
- Adaptive UI density
- Enhanced performance

---

**Thank you for using Pxgate!** 📸✨

For the best experience, use keyboard shortcuts and explore the professional UI features.

# Installation Guide

## 📥 Download

Go to the [Releases page](https://github.com/yourusername/VibeCulling/releases) and download the appropriate version for your system:

- **Windows**: `Pxgate-Windows.zip`
- **macOS Intel**: `Pxgate-macOS-Intel.zip` (for Intel-based Macs)
- **macOS Apple Silicon**: `Pxgate-macOS-AppleSilicon.zip` (for M1/M2/M3 Macs)

**Not sure which Mac you have?**
- Click the Apple menu () → About This Mac
- Look for "Chip" or "Processor"
  - If it says "Apple M1", "M2", or "M3" → Download **Apple Silicon** version
  - If it says "Intel" → Download **Intel** version

---

## 🪟 Windows Installation

1. **Download** `Pxgate-Windows.zip`
2. **Extract** the zip file to a folder (e.g., `C:\Program Files\Pxgate`)
3. **Run** `pxgate.exe`

**That's it!** No Python or additional software needed.

### Optional: Create Desktop Shortcut
- Right-click on `pxgate.exe`
- Select "Create shortcut"
- Drag the shortcut to your Desktop

---

## 🍎 macOS Installation

### Step 1: Download
Download the appropriate version:
- **Intel Macs**: `Pxgate-macOS-Intel.zip`
- **Apple Silicon Macs**: `Pxgate-macOS-AppleSilicon.zip`

### Step 2: Extract
Double-click the downloaded zip file to extract `Pxgate.app`

### Step 3: Install
Drag `Pxgate.app` to your **Applications** folder

### Step 4: First Launch (Important!)

Because the app is not signed with an Apple Developer certificate, you'll see a security warning on first launch.

**You'll see:**
> "Pxgate.app can't be opened because it is from an unidentified developer"

**To fix this:**
1. **Right-click** (or Control-click) on `Pxgate.app`
2. Select **"Open"** from the menu
3. Click **"Open"** in the dialog that appears

**The app will now run normally!** You only need to do this once.

### Alternative Method:
1. Go to **System Settings** → **Privacy & Security**
2. Scroll down to the Security section
3. Click **"Open Anyway"** next to the Pxgate warning
4. Click **"Open"** to confirm

---

## ✅ System Requirements

### Windows
- **OS**: Windows 10 or later (64-bit)
- **RAM**: 4 GB minimum, 8 GB recommended
- **Storage**: 500 MB free space
- **Display**: 1920x1080 or higher recommended

### macOS Intel
- **OS**: macOS 10.15 Catalina or later
- **RAM**: 4 GB minimum, 8 GB recommended
- **Storage**: 500 MB free space
- **Display**: 1920x1080 or higher recommended

### macOS Apple Silicon
- **OS**: macOS 11.0 Big Sur or later
- **RAM**: 4 GB minimum, 8 GB recommended
- **Storage**: 500 MB free space
- **Display**: 1920x1080 or higher recommended

---

## 🚀 First Run

After installation:

1. **Launch** the application
2. **Click** "📁 Open Folder" in the toolbar
3. **Select** a folder containing your images
4. **Start culling!**

---

## 🆘 Troubleshooting

### Windows: "Windows protected your PC" warning

**This is normal for unsigned applications.**

1. Click **"More info"**
2. Click **"Run anyway"**

### macOS: "Pxgate.app is damaged and can't be opened"

**This happens if you didn't right-click → Open on first launch.**

**Solution:**
1. Delete the app
2. Re-download and extract
3. **Right-click** → **Open** (don't double-click!)

### macOS: App won't open at all

**Try removing the quarantine attribute:**

1. Open **Terminal** (Applications → Utilities → Terminal)
2. Type: `xattr -cr ` (with a space at the end)
3. Drag `Pxgate.app` into the Terminal window
4. Press Enter
5. Try opening the app again

### App crashes on startup

**Check system requirements:**
- Ensure your OS version is supported
- Ensure you have enough free RAM
- Try restarting your computer

**Still having issues?**
- Check the [Issues page](https://github.com/yourusername/VibeCulling/issues)
- Create a new issue with details about your system

---

## 🔄 Updating

To update to a new version:

1. **Download** the latest release
2. **Replace** the old version with the new one
3. **Windows**: Replace the entire `pxgate` folder
4. **macOS**: Replace `Pxgate.app` in Applications

Your settings and preferences are stored separately and will be preserved.

---

## 🗑️ Uninstalling

### Windows
1. Delete the `pxgate` folder
2. Delete the desktop shortcut (if created)

### macOS
1. Drag `Pxgate.app` to the Trash
2. Empty the Trash

**Optional**: Remove settings
- Windows: Delete `C:\Users\YourName\AppData\Roaming\Pxgate`
- macOS: Delete `~/Library/Application Support/Pxgate`

---

## 📞 Support

- **Documentation**: [GitHub Wiki](https://github.com/yourusername/VibeCulling/wiki)
- **Issues**: [GitHub Issues](https://github.com/yourusername/VibeCulling/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/VibeCulling/discussions)

---

## ⚡ Quick Start Tips

1. **Keyboard shortcuts**: 
   - `Left/Right arrows`: Navigate images
   - `1-9`: Move to folder 1-9
   - `G`: Toggle grid view
   - `T`: Toggle thumbnails
   - `F1`: Fit to window
   - `F2`: 100% zoom

2. **Grid mode**: Press `G` to view multiple images at once

3. **Thumbnails**: Press `T` to show/hide the thumbnail panel

4. **Drag & drop**: Drag images to folders to organize them

Enjoy using Pxgate! 🎉

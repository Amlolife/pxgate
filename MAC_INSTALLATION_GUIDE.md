# Pxgate - Mac Installation Guide

## For Mac M-Chip Users (M1, M2, M3, M4)

### Quick Start

1. **Download** the Pxgate-macOS-M-Chip.dmg file
2. **Open** the DMG file
3. **Drag** Pxgate.app to your Applications folder
4. **Right-click** on Pxgate.app and select "Open" (first time only)
5. **Click** "Open" in the security dialog

---

## First Launch (Important!)

### Gatekeeper Security

On first launch, macOS will block the app because it's not signed with an Apple Developer certificate.

**DO NOT** double-click to open the first time!

**Instead:**
1. Right-click (or Control+click) on Pxgate.app
2. Select "Open" from the menu
3. Click "Open" in the security dialog
4. The app will launch

After the first launch, you can open it normally by double-clicking.

### Alternative Method

If right-click doesn't work:
1. Go to **System Settings** → **Privacy & Security**
2. Scroll down to find "Pxgate was blocked"
3. Click **"Open Anyway"**
4. Confirm by clicking **"Open"**

---

## Troubleshooting

### "App is already running" Error

**This issue is now fixed in version 25.08.06+**

If you still see this error:
1. Open **Activity Monitor** (Applications → Utilities)
2. Search for "Pxgate"
3. Select it and click the **X** button to quit
4. Try launching again

Or use Terminal:
```bash
rm ~/Library/Application\ Support/Pxgate/pxgate.lock
```

### App Won't Open

**Check if you're on Apple Silicon:**
```bash
uname -m
```
- If it shows `arm64` → You have Apple Silicon (M-chip) ✓
- If it shows `x86_64` → You have Intel Mac

**For Intel Macs:** Download the Intel version instead, or the M-chip version will run via Rosetta 2 (slower).

### Performance Issues

**Verify you're running native ARM64:**
1. Open **Activity Monitor**
2. Find "Pxgate" in the list
3. Check the "Kind" column:
   - **"Apple"** = Native ARM64 (best performance) ✓
   - **"Intel"** = Running via Rosetta 2 (slower)

If it shows "Intel", you may have downloaded the wrong version.

### Logs Location

If you experience crashes or issues, check the logs:
```
~/Library/Application Support/Pxgate/logs/
```

Open in Finder:
```bash
open ~/Library/Application\ Support/Pxgate/logs/
```

---

## System Requirements

### Minimum Requirements
- **macOS**: 11.0 (Big Sur) or later
- **RAM**: 8 GB
- **Storage**: 500 MB free space
- **Processor**: Apple M1 or later (or Intel with Rosetta 2)

### Recommended
- **macOS**: 12.0 (Monterey) or later
- **RAM**: 16 GB or more
- **Storage**: 2 GB free space
- **Processor**: Apple M1 Pro/Max or later

---

## Features Optimized for M-Chip

✅ **Native ARM64 Performance**
- No Rosetta 2 translation overhead
- Full Metal GPU acceleration via Qt
- Efficient memory usage

✅ **Multi-Core RAW Processing**
- Automatically uses multiple CPU cores
- M1/M2 (8 cores): 2 decoder processes
- M1 Pro/Max (10+ cores): 3-4 decoder processes

✅ **Low Power Consumption**
- Optimized for Apple Silicon efficiency
- Minimal battery drain on MacBooks

---

## Uninstalling

To completely remove Pxgate:

1. **Delete the app:**
   ```bash
   rm -rf /Applications/Pxgate.app
   ```

2. **Remove app data:**
   ```bash
   rm -rf ~/Library/Application\ Support/Pxgate
   ```

3. **Remove preferences (optional):**
   ```bash
   rm ~/Library/Preferences/com.pxgate.app.plist
   ```

---

## Privacy & Permissions

Pxgate may request the following permissions:

- **Files and Folders**: To read and organize your photos
- **Full Disk Access**: Only if you want to access protected folders

You can manage these in:
**System Settings** → **Privacy & Security** → **Files and Folders**

---

## Keyboard Shortcuts

### Navigation
- **Arrow Keys**: Navigate between images
- **Space**: Toggle selection
- **Cmd + A**: Select all
- **Cmd + D**: Deselect all

### Actions
- **Number Keys (1-9)**: Move to corresponding folder
- **Delete/Backspace**: Move to trash
- **Cmd + Z**: Undo last move
- **Cmd + Y**: Redo move

### View
- **Cmd + +**: Zoom in
- **Cmd + -**: Zoom out
- **Cmd + 0**: Fit to window
- **F**: Toggle fullscreen

---

## Support

### Getting Help

1. **Check the logs** (see Logs Location above)
2. **Restart the app**
3. **Restart your Mac**
4. **Report issues** with log files attached

### Known Issues

- First launch requires right-click → Open (macOS security)
- Some RAW formats may require additional processing time
- Large image collections (10,000+) may take time to load thumbnails

---

## Updates

To update Pxgate:
1. Download the latest version
2. Quit the current version
3. Replace the old app in Applications folder
4. Launch the new version

Your settings and preferences will be preserved.

---

## Performance Tips

### For Best Performance

1. **Use SSD storage** for your photo library
2. **Close other apps** when processing large RAW files
3. **Increase RAM** if working with 50+ MP images
4. **Keep macOS updated** for latest Metal optimizations

### RAW File Performance

| Camera Resolution | Recommended RAM | Load Time (M1) |
|-------------------|-----------------|----------------|
| 24 MP | 8 GB | < 1 second |
| 45 MP | 16 GB | 1-2 seconds |
| 61 MP | 32 GB | 2-3 seconds |
| 100 MP | 64 GB | 3-5 seconds |

---

## Compatibility

### Supported File Formats

**RAW Formats:**
- Canon: .CR2, .CR3
- Nikon: .NEF, .NRW
- Sony: .ARW
- Fujifilm: .RAF
- Olympus: .ORF
- Panasonic: .RW2
- Pentax: .PEF, .DNG
- And many more...

**Standard Formats:**
- JPEG (.jpg, .jpeg)
- PNG (.png)
- TIFF (.tif, .tiff)
- HEIF/HEIC (.heic, .heif)
- BMP (.bmp)
- WebP (.webp)

---

## Questions?

This is a photo culling tool designed to help you quickly sort through large photo collections. It's optimized for professional photographers working with RAW files on Apple Silicon Macs.

Enjoy fast, efficient photo culling! 📸

# Pxgate - Cross-Platform Support

## ✅ Supported Platforms

Pxgate works on:
- **Windows** (7, 8, 10, 11)
- **macOS** (10.13+)
- **Linux** (Ubuntu, Fedora, etc.)

---

## 🖼️ Application Icons

### Windows & Linux
- **File**: `app_icon.ico` ✓ Already created
- **Format**: ICO with multiple sizes (16, 32, 48, 64, 128, 256px)
- **Status**: Ready to use!

### macOS
- **File**: `app_icon.icns` (needs to be created on macOS)
- **Source**: `app_icon.iconset/` folder ✓ Already created
- **How to create**:
  ```bash
  iconutil -c icns app_icon.iconset
  ```
  This will create `app_icon.icns` from the iconset folder.

---

## 📦 Installation

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python VibeCulling.py
```

---

## 🔧 Platform-Specific Features

### Windows
- Dark title bar support
- Single instance lock using `msvcrt`
- App data: `C:\Users\<Username>\AppData\Roaming\Pxgate`

### macOS
- Native dark mode support
- Single instance lock using `fcntl`
- App data: `~/Library/Application Support/Pxgate`
- **Note**: On macOS, run the iconutil command to create app_icon.icns

### Linux
- Single instance lock using `fcntl`
- App data: `~/.config/Pxgate`

---

## 🎨 New Modern UI

The app features a modernized UI with:
- Modern blue accent color (#6B9BD1)
- Rounded corners (6px)
- Better contrast and readability
- Smooth hover effects
- Professional look and feel

---

## 📝 Building Executables

### Windows (PyInstaller)
```bash
pyinstaller --name=Pxgate --windowed --icon=app_icon.ico VibeCulling.py
```

### macOS (PyInstaller)
```bash
# First create the .icns file:
iconutil -c icns app_icon.iconset

# Then build:
pyinstaller --name=Pxgate --windowed --icon=app_icon.icns VibeCulling.py
```

### Linux (PyInstaller)
```bash
pyinstaller --name=Pxgate --windowed --icon=app_icon.ico VibeCulling.py
```

---

## 🆘 Troubleshooting

### Missing Dependencies
If you get module errors, install all requirements:
```bash
pip install -r requirements.txt
```

### Icon Not Showing on macOS
Make sure you've created the .icns file:
```bash
iconutil -c icns app_icon.iconset
```

### App Already Running Error
The app uses single-instance locking. Close any existing instances before starting a new one.

---

## 📄 License
AGPL-3.0 - See source code for details

# -*- mode: python ; coding: utf-8 -*-
# This is a consolidated spec file for building on all platforms.
# It contains specific logic to handle macOS PySide6 framework issues.

from PyInstaller.utils.hooks import collect_all
import sys

# --- Common Configuration ---
_datas = []
_binaries = []
_hidden = [
    'rawpy', 'PIL', 'PIL.Image', 'PIL.ExifTags', 'exifread',
    'PIL._tkinter_finder',
]

# Collect all necessary third-party packages
for m in ('rawpy', 'PySide6', 'pillow_heif'):
    tmp = collect_all(m)
    _datas += tmp[0]
    _binaries += tmp[1]
    _hidden += tmp[2]

# Add qt.conf for macOS to find plugins correctly
if sys.platform == 'darwin':
    _datas += [('qt.conf', '.')]

# --- Analysis Step ---
a = Analysis(
    ['pxgate.py'],
    pathex=[],
    binaries=_binaries,
    datas=_datas,
    hiddenimports=_hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],  # Excludes are handled manually for macOS below
    noarchive=False,
    optimize=0,
)

# --- macOS Specific Filtering ---
# This block is critical to prevent the FileExistsError on macOS.
# It manually removes problematic Qt frameworks from the list of binaries.
if sys.platform == 'darwin':
    qt_frameworks_to_exclude = [
        'Qt3DAnimation', 'Qt3DCore', 'Qt3DExtras', 'Qt3DInput', 'Qt3DLogic',
        'Qt3DRender', 'QtBluetooth', 'QtCharts', 'QtDataVisualization',
        'QtNetworkAuth', 'QtNfc', 'QtSensors', 'QtSerialBus', 'QtSerialPort',
        'QtWebEngineCore', 'QtWebEngineWidgets', 'QtWebSockets', 'QtWebChannel',
        'QtWebEngineQuick'
    ]
    
    filtered_binaries = []
    for b in a.binaries:
        # b[0] is the destination path in the bundle
        if not any(f'{framework}.framework' in b[0] for framework in qt_frameworks_to_exclude):
            filtered_binaries.append(b)
    
    # Overwrite the original binaries list with the filtered one
    a.binaries = filtered_binaries


# --- Bundling Steps ---
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Pxgate',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to True for debugging, False for release
    icon='app_icon.ico' if sys.platform == 'win32' else None
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Pxgate',
)

# --- Final App Bundle (macOS only) ---
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='Pxgate.app',
        icon='app_icon.icns',
        bundle_identifier=None,
    )

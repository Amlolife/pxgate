# -*- mode: python ; coding: utf-8 -*-
# This is a simplified spec file based on the working 'Vibe Origin' example.
# It allows PyInstaller to automatically handle PySide6 dependencies.

from PyInstaller.utils.hooks import collect_all
import sys

# --- Collect Data and Dependencies ---
# We let PyInstaller find PySide6, but explicitly collect other packages.
datas = []
binaries = []
hiddenimports = []

for pkg in ['rawpy', 'pillow_heif', 'exifread']:
    tmp = collect_all(pkg)
    datas += tmp[0]
    binaries += tmp[1]
    hiddenimports += tmp[2]

# Add the icon based on the platform
if sys.platform == 'win32':
    datas += [('app_icon.ico', '.')]

# --- Analysis Step ---
a = Analysis(
    ['pxgate.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

# --- Bundling Steps ---
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Pxgate',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
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

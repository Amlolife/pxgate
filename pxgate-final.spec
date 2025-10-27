# -*- mode: python ; coding: utf-8 -*-
# This is the definitive spec file to fix the macOS build issue.
# It manually collects PySide6 components instead of using collect_all().

from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs
import sys

# --- Manual PySide6 Collection ---
# This is the key to the fix. We manually collect only what's needed.
_binaries = []
_datas = []
_hidden = []

if sys.platform == 'darwin':
    # Manually collect the essential Qt libraries
    for lib in ['QtCore', 'QtGui', 'QtWidgets']:
        _binaries += collect_dynamic_libs('PySide6', f'Qt/lib/{lib}.framework')

    # Manually collect the required platform plugin
    _datas += collect_data_files('PySide6', 'Qt/plugins/platforms', destdir='PySide6/Qt/plugins/platforms')
    
    # Add the qt.conf file
    _datas += [('qt.conf', '.')]
else:
    # For other platforms, use the standard collection method
    from PyInstaller.utils.hooks import collect_all
    pyside_all = collect_all('PySide6')
    _datas += pyside_all[0]
    _binaries += pyside_all[1]
    _hidden += pyside_all[2]

# --- Collect Other Dependencies ---
from PyInstaller.utils.hooks import collect_all
for m in ('rawpy', 'pillow_heif'):
    tmp = collect_all(m)
    _datas += tmp[0]
    _binaries += tmp[1]
    _hidden += tmp[2]

_hidden += ['rawpy', 'PIL', 'PIL.Image', 'PIL.ExifTags', 'exifread', 'PIL._tkinter_finder']

# --- Analysis Step ---
a = Analysis(
    ['pxgate.py'],
    pathex=[],
    binaries=_binaries,
    datas=_datas,
    hiddenimports=list(set(_hidden)), # Use set to remove duplicates
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
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
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

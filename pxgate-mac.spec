# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

# Collect third-party resources
_datas = []
_binaries = []
_hidden = [
    'rawpy', 'PIL', 'PIL.Image', 'PIL.ExifTags', 'exifread',
    'PIL._tkinter_finder',
]

# Add qt.conf so Qt finds PlugIns inside the .app bundle
_datas += [('qt.conf', '.')]

for m in ('rawpy', 'PySide6', 'pillow_heif'):
    tmp = collect_all(m)
    _datas += tmp[0]; _binaries += tmp[1]; _hidden += tmp[2]


a = Analysis(
    ['pxgate.py'],
    pathex=[],
    binaries=_binaries,
    datas=_datas,
    hiddenimports=_hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'PySide6.Qt3DAnimation',
        'PySide6.Qt3DCore',
        'PySide6.Qt3DExtras',
        'PySide6.Qt3DInput',
        'PySide6.Qt3DLogic',
        'PySide6.Qt3DRender',
        'PySide6.QtBluetooth',
        'PySide6.QtCharts',
        'PySide6.QtDataVisualization',
        'PySide6.QtNetworkAuth',
        'PySide6.QtNfc',
        'PySide6.QtSensors',
        'PySide6.QtSerialBus',
        'PySide6.QtSerialPort',
        'PySide6.QtWebEngineCore',
        'PySide6.QtWebEngineWidgets',
        'PySide6.QtWebSockets',
        'PySide6.QtWebChannel',
        'PySide6.QtWebEngineQuick',
    ],
    noarchive=False,
    optimize=0,
)

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

app = BUNDLE(
    coll,
    name='Pxgate.app',
    icon=None,
    bundle_identifier=None,
)

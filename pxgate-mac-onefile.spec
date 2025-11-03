# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

# Collect third-party resources
_datas = []
_binaries = []
_hidden = [
    'rawpy', 'PIL', 'PIL.Image', 'PIL.ExifTags', 'exifread',
    'PIL._tkinter_finder',
]

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
    a.binaries,
    a.datas,
    [],
    name='Pxgate',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

app = BUNDLE(
    exe,
    name='Pxgate.app',
    icon=None,
    bundle_identifier='com.pxgate.app',
    info_plist={
        'CFBundleShortVersionString': '25.08.06',
        'CFBundleVersion': '25.08.06',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '11.0',
    },
)

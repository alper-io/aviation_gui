# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.'],
    pathex=['/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages'],
    binaries=[],
    datas=[('/Users/yigityilmaz/PycharmProjects/AvASysProject/src', 'src'), ('/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/customtkinter', 'customtkinter')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
app = BUNDLE(
    coll,
    name='main.app',
    icon=None,
    bundle_identifier=None,
)

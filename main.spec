# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/Users/ugn/Documents/Code/Commercial/overtitle/overtitle-build/main.py'],
    pathex=[],
    binaries=[],
    datas=[('/Users/ugn/Documents/Code/Commercial/overtitle/overtitle-build/templates', 'templates/'), ('/Users/ugn/Documents/Code/Commercial/overtitle/overtitle-build/static', 'static/'), ('/Users/ugn/Documents/Code/Commercial/overtitle/overtitle-build/env/lib/python3.9/site-packages/customtkinter', 'customtkinter/'), ('/Users/ugn/Documents/Code/Commercial/overtitle/overtitle-build/env/lib/python3.9/site-packages/iso639', 'iso639/'), ('/Users/ugn/Documents/Code/Commercial/overtitle/overtitle-build/app.py', '.'), ('/Users/ugn/Documents/Code/Commercial/overtitle/overtitle-build/requirements.txt', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

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
    icon=['/Users/ugn/Documents/Code/Commercial/overtitle/overtitle-build/favicon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
app = BUNDLE(
    coll,
    name='main.app',
    icon='/Users/ugn/Documents/Code/Commercial/overtitle/overtitle-build/favicon.ico',
    bundle_identifier=None,
)

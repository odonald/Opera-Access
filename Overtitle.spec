# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('/Users/ugn/Documents/Code/Commercial/overtitle/overtitle-build/env/lib/python3.9/site-packages/iso639', 'iso639/'), ('/Users/ugn/Documents/Code/Commercial/overtitle/overtitle-build/templates', 'templates/'), ('/Users/ugn/Documents/Code/Commercial/overtitle/overtitle-build/static', 'static/')],
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
    a.binaries,
    a.datas,
    [],
    name='Overtitle',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['/Users/ugn/Documents/Code/Commercial/overtitle/overtitle-build/favicon.icns'],
)
app = BUNDLE(
    exe,
    name='Overtitle.app',
    icon='/Users/ugn/Documents/Code/Commercial/overtitle/overtitle-build/favicon.icns',
    bundle_identifier=None,
)

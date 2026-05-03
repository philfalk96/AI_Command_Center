# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['p:\\Code\\Source_Code\\ai-ui-system\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('p:\\Code\\Source_Code\\ai-ui-system\\config', 'config'), ('p:\\Code\\Source_Code\\ai-ui-system\\avatar', 'avatar'), ('p:\\Code\\Source_Code\\ai-ui-system\\backgrounds', 'backgrounds'), ('p:\\Code\\Source_Code\\ai-ui-system\\ui\\dashboard.html', 'ui')],
    hiddenimports=['uvicorn', 'fastapi', 'whisper', 'edge_tts', 'pyttsx3'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ai-ui-system',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ai-ui-system',
)

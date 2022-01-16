# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

import os, pygame_gui
pygame_data_loc = os.path.join(os.path.dirname(pygame_gui.__file__), 'data')
path_theme = os.path.join('resources', 'themes')
font_path = os.path.join('resources', 'fonts')

a = Analysis(['sway.py'],
             pathex=[],
             binaries=[],
             datas=[(os.path.join(font_path, 'rusmadeinchinav2.ttf'), 'resources/fonts'),
                    (os.path.join(font_path, 'HanZi.ttf'), 'resources/fonts'),
                    (os.path.join(path_theme, 'sway_theme.json'), 'resources/themes'),
                    (pygame_data_loc, os.path.join('pygame_gui', 'data'))],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='sway',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['proxy_util\\proxy_result_dialog.py'],
             pathex=['C:\\Users\\Zuber\\PycharmProjects\\mitmproxy_client', '', 'C:\\Users\\Zuber\\PycharmProjects\\mitmproxy_client'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
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
          name='proxy_result_dialog',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )

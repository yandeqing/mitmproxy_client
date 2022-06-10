#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/7/5 14:25
'''
# This collects all dynamically imported scrapy modules and data files.
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

hiddenimports = (collect_submodules('mitmproxy') +
                 collect_submodules('mitmproxy.tools')
                 )
datas = collect_data_files('mitmproxy')

# default.py - main module.
#
# Copyright 2015 kharts (https://github.com/kharts)
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version

"""
default.py - main module of the plugin.
"""

__author__ = 'kharts'

import sys
import os

import xbmcaddon
import xbmc

#importing uatv module
uatv_addon = xbmcaddon.Addon()
uatv_path = uatv_addon.getAddonInfo("path")
sys.path.append(xbmc.translatePath(os.path.join(uatv_path, "resources", "lib")))
import uatv

uatv.start()

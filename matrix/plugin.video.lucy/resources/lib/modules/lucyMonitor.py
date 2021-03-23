# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import xbmcaddon

from resources.lib.modules.globals import g

try:
    import xbmc
except ImportError:
    from mock_kodi import xbmc


class lucyMonitor(xbmc.Monitor):
    def onSettingsChanged(self):
        super(lucyMonitor, self).onSettingsChanged()
        g.ADDON = xbmcaddon.Addon()
        if not g.is_addon_visible():
            return
        g.trigger_widget_refresh()

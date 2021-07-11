# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon

properties = [
    "context.halibut.quickResume",
    "context.halibut.shuffle",
    "context.halibut.playFromRandomPoint",
    "context.halibut.rescrape",
    "context.halibut.sourceSelect",
    "context.halibut.findSimilar",
    "context.halibut.browseShow",
    "context.halibut.browseSeason",
    "context.halibut.traktManager",
]


class PropertiesUpdater(xbmc.Monitor):
    def __init__(self):
        super(PropertiesUpdater, self).__init__()
        self.addon = xbmcaddon.Addon()
        self._update_window_properties()

    def __del__(self):
        del self.addon

    def onSettingsChanged(self):
        self._update_window_properties()

    def _update_window_properties(self):
        for prop in properties:
            setting = self.addon.getSetting(prop)
            if setting == "false":
                xbmc.executebuiltin("SetProperty({},{},home)".format(prop, setting))
            else:
                xbmc.executebuiltin("ClearProperty({},home)".format(prop))
            xbmc.log(
                "Context menu item {}: {}".format(
                    "disabled" if setting == "false" else "enabled", prop
                )
            )


xbmc.log("context.halibut service: starting", xbmc.LOGINFO)

try:
    # start monitoring settings changes events
    properties_monitor = PropertiesUpdater()

    # wait until abort is requested
    properties_monitor.waitForAbort()
except Exception as e:
    xbmc.log("context.halibut service: error - {}".format(e), xbmc.LOGERROR)
finally:
    del properties_monitor

xbmc.log("context.halibut service: stopped", xbmc.LOGINFO)

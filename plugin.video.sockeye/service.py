# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import sqlite3
import sys
from random import randint

import xbmc

from resources.lib.common import tools

if tools.is_stub():
    # noinspection PyUnresolvedReferences
    from mock_kodi import MOCK

from resources.lib.modules.globals import g

from resources.lib.common import maintenance
from resources.lib.database.trakt_sync.activities import TraktSyncDatabase
from resources.lib.modules.sockeyeMonitor import sockeyeMonitor
from resources.lib.modules.update_news import do_update_news
from resources.lib.modules.manual_timezone import validate_timezone_detected

g.init_globals(sys.argv)
g.HOME_WINDOW.setProperty("sockeyeDownloadManagerIndex", "{}")

g.log("##################  STARTING SERVICE  ######################")
g.log("### {} {}".format(g.ADDON_ID, g.VERSION))
g.log("### PLATFORM: {}".format(g.PLATFORM))
g.log("### SQLite: {}".format(sqlite3.sqlite_version))  # pylint: disable=no-member
g.log("### Detected Kodi Version: {}".format(g.KODI_VERSION))
g.log("### Detected timezone: {}".format(repr(g.LOCAL_TIMEZONE.zone)))
g.log("#############  SERVICE ENTERED KEEP ALIVE  #################")

monitor = sockeyeMonitor()
try:
    xbmc.executebuiltin(
        'RunPlugin("plugin://plugin.video.sockeye/?action=longLifeServiceManager")'
    )

    do_update_news()
    validate_timezone_detected()
    try:
        g.clear_kodi_bookmarks()
    except TypeError:
        g.log(
            "Unable to clear bookmarks on service init. This is not a problem if it occurs immediately after install.",
            "warning"
        )

    # Disable the restoration of reuselanguageinvoker addon.xml based on settings value on upgrade.
    # It can still be toggled in settings although initially it will show user's last setting value
    # This is in preparation for removal of user setting/toggle.
    # maintenance.toggle_reuselanguageinvoker(
    #     True if g.get_setting("reuselanguageinvoker.status") == "Enabled" else False)

    g.wait_for_abort(30)  # Sleep for a half a minute to allow widget loads to complete.
    while not monitor.abortRequested():
        try:
            if g.get_bool_setting("general.checkAddonUpdates"):
                maintenance.check_for_addon_update()

            maintenance.run_maintenance()
            TraktSyncDatabase().sync_activities()
        except Exception:
            g.log("Background service failure", "error")
            g.log_stacktrace()
        if g.wait_for_abort(60 * randint(13, 17)):
            break
finally:
    del monitor
    g.deinit()
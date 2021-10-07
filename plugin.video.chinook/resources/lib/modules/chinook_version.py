# -*- coding: utf-8 -*-
from resources.lib.modules.globals import g


def do_version_change():
    if g.get_setting("chinook.version") == g.CLEAN_VERSION:
        return

    g.log("Clearing cache on chinook version change", "info")
    g.clear_cache(silent=True)

    g.set_setting("chinook.version", g.CLEAN_VERSION)

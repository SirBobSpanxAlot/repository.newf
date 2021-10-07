# -*- coding: utf-8 -*-
from resources.lib.modules.globals import g


def do_version_change():
    if g.get_setting("halibut.version") == g.CLEAN_VERSION:
        return

    g.log("Clearing cache on halibut version change", "info")
    g.clear_cache(silent=True)

    g.set_setting("halibut.version", g.CLEAN_VERSION)

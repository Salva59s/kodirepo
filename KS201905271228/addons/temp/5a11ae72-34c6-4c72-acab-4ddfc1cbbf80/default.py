# -*- coding: utf-8 -*-
#------------------------------------------------------------
# streamondemand-pureita
# Copyright 2015 tvalacarta@gmail.com
#
# Distributed under the terms of GNU General Public License v3 (GPLv3)
# http://www.gnu.org/licenses/gpl-3.0.html
#------------------------------------------------------------
# This file is part of streamondemand-pureita.
#
# streamondemand-pureita is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# streamondemand-pureita is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with streamondemand-pureita.  If not, see <http://www.gnu.org/licenses/>.
#------------------------------------------------------------

import os

import sys
import plugintools
import navigation
from core import updater
from core.item import Item
from core import config

plugintools.application_log_enabled = (plugintools.get_setting("debug")=="true")
plugintools.module_log_enabled = (plugintools.get_setting("debug")=="true")
plugintools.http_debug_log_enabled = (plugintools.get_setting("debug")=="true")

plugintools.log("stream on demand pureita 1 begin")

librerias = xbmc.translatePath( os.path.join( config.get_runtime_path(), 'lib' ) )
sys.path.append (librerias)

updater.checkforupdates(plugin_mode=False)

# Get items for main menu
item = Item( channel="navigation", action="mainlist" )
itemlist = navigation.get_next_items( item )

# Open main window
window = navigation.get_window_for_item( item )
window.setParentItem(item)
window.setItemlist(itemlist)
window.doModal()
del window

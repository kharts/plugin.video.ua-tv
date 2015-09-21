# uatv.py - with functions for watching Ukrainian TV Channels.
#
# Copyright 2015 kharts (https://github.com/kharts)
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

"""
uatv.py - module with functions for watching Ukrainian TV Channels.
Public functions:
index() - opens main menu of the plugin.

add_channel_to_menu(name) - adds channel to the main menu of the plugin.
"""

__author__ = 'kharts'

import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmc
import sys

addon = xbmcaddon.Addon()
addonID = addon.getAddonInfo('id')
channelsDB = {}
pluginhandle = int(sys.argv[1])

def index():
    """
    Opens main manu of the plugin.
    :return: None
    """

    debug("index")
    for channel_id in channelsDB:
        channel = channelsDB[channel_id]
        add_channel_to_menu(name=channel["name"])
    xbmcplugin.endOfDirectory(pluginhandle)


def add_channel_to_menu(name):
    """
    Adds channel to the main menu of the plugin
    :param name: - name of channel
    :return: None
    """

    listItem = xbmcgui.ListItem(name)
    url = ""
    xbmcplugin.addDirectoryItem(handle=pluginhandle, url=url, listitem=listItem)


def update_channels_db():
    """
    Updates channelsDB
    :rtype : None
    :return: None
    """

    add_channel_to_db(id="1stnational",
                      name=translate(30001))


def add_channel_to_db(id, name):
    """
    Adds channel to channelsDB
    :param id: id channel's id
    :param name: name of channel (in local language)
    :return: None
    """

    channelsDB[id] = {"name": name}


def translate(id):
    """
    Gets translation of string with given id
    :rtype : str
    :param id: identifier of string
    :return: translation for local language
    """

    return addon.getLocalizedString(id)

def debug(content):
    """
    Outputs content to log file
    :param content: content which should be output
    :return: None
    """
    log(unicode(content), xbmc.LOGDEBUG)

def log(msg, level=xbmc.LOGNOTICE):
    """
    Outputs message to log file
    :param msg: message to output
    :param level: debug levelxbmc. Values:
    xbmc.LOGDEBUG = 0
    xbmc.LOGERROR = 4
    xbmc.LOGFATAL = 6
    xbmc.LOGINFO = 1
    xbmc.LOGNONE = 7
    xbmc.LOGNOTICE = 2
    xbmc.LOGSEVERE = 5
    xbmc.LOGWARNING = 3
    """

    log_message = u'{0}: {1}'.format(addonID, msg)
    xbmc.log(log_message.encode("utf-8"), level)


update_channels_db()
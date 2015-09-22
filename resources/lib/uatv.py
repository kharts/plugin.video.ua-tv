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
import os

addon = xbmcaddon.Addon()
addonID = addon.getAddonInfo('id')
addonFolder = xbmc.translatePath('special://home/addons/'+addonID).decode('utf-8')
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
        add_channel_to_menu(name=channel["name"],
                            icon=channel["icon"])
    xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(pluginhandle)


def add_channel_to_menu(name, icon):
    """
    Adds channel to the main menu of the plugin
    :param name: - name of channel
    :return: None
    """
    iconImage = image_path(icon)
    listItem = xbmcgui.ListItem(name, iconImage=iconImage)
    url = ""
    xbmcplugin.addDirectoryItem(handle=pluginhandle, url=url, listitem=listItem)


def update_channels_db():
    """
    Updates channelsDB
    :rtype : None
    :return: None
    """

    add_channel_to_db(id="1stnational",
                      name=translate(30001),
                      icon="1stnational.jpg")
    add_channel_to_db(id="112channel",
                      name=translate(30002),
                      icon="112channel.png")
    add_channel_to_db(id="24channel",
                      name=translate(30003),
                      icon="24channel.png")
    add_channel_to_db(id="5channel",
                      name=translate(30004),
                      icon="5channel.png")
    add_channel_to_db(id="espresotv",
                      name=translate(30005),
                      icon="espresotv.png")
    add_channel_to_db(id="hromadsketv",
                      name=translate(30006),
                      icon="hromadsketv.jpg")
    add_channel_to_db(id="ubr",
                      name=translate(30007),
                      icon="ubr.png")


def add_channel_to_db(id, name, icon):
    """
    Adds channel to channelsDB
    :param id: id channel's id
    :param name: name of channel (in local language)
    :return: None
    """

    channelsDB[id] = {"name": name, "icon": icon}


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


def image_path(name):
    """
    Gets full path to image
    :param name: short name of image
    :return: full filename of image
    """

    resourcesFolder = os.path.join(addonFolder, "resources")
    imagesFolder = os.path.join(resourcesFolder, "img")
    return os.path.join(imagesFolder, name)


update_channels_db()
# uatv.py - with functions for watching Ukrainian TV Channels.
#
# Copyright 2015 kharts (https://github.com/kharts)
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

"""
uatv.py - module with functions for watching Ukrainian TV Channels.

Public functions:

start() - starts plugin
"""

__author__ = 'kharts'

import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmc
import sys
import os
import urllib
import urllib2
import urlparse

addon = xbmcaddon.Addon()
addonID = addon.getAddonInfo('id')
addonFolder = xbmc.translatePath('special://home/addons/'+addonID).decode('utf-8')
channelsDB = {}
pluginhandle = int(sys.argv[1])

#importing youtube plugin
youtube_addon = xbmcaddon.Addon("plugin.video.youtube")
youtube_path = youtube_addon.getAddonInfo("path")
sys.path.insert(0, xbmc.translatePath(youtube_path))
from resources.lib.youtube.client import YouTube
youtube_client = YouTube()


def start():
    """
    Starts plugin
    :return: None
    """

    debug(sys.argv[2])
    params = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)
    if "channel_id" in params:
        open_channel(params["channel_id"][0])
    else:
        list_channels()


def list_channels():
    """
    Opens main manu of the plugin.
    :return: None
    """

    debug("index")
    for channel_id in channelsDB:
        channel = channelsDB[channel_id]
        add_channel_to_menu(id=channel_id,
                            name=channel["name"],
                            icon=channel["icon"])
    xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(pluginhandle)


def open_channel(channel_id):
    """
    Opens video stream of given channel
    :param channel_id: id of the channel
    :return: None
    """

    channel = channelsDB[channel_id]
    channel_type = channel["type"]
    if channel_type == "youtube":
        open_youtube_channel(channel)
    elif channel_type == "ictv":
        open_ictv(channel)
    elif channel_type == "ukraina":
        open_ukraina(channel)


def open_youtube_channel(channel):
    """
    Opens youtube channel
    :param channel: - channel to open (from channelsDB)
    :return: None
    """

    youtube_channel_id = channel["youtube_channel_id"]
    video_id = channel["video_id"]
    if not video_id:
        if not youtube_channel_id:
            username = channel["username"]
            if not username:
                debug("No channel id and username")
                return
            youtube_channel_id = get_channel_id_by_username(username)
            if not youtube_channel_id:
                return
            else:
                channel["youtube_channel_id"]=youtube_channel_id
        video_id = get_live_stream_id(youtube_channel_id)
    if not video_id:
        error(translate(30010))
        return
    else:
        channel["video_id"] = video_id
    xbmc.Player().play("plugin://plugin.video.youtube/play/?video_id=" + video_id)


def open_ictv(channel):
    """
    Opens ICTV channel's live stream
    :param channel: channel to open (from channelsDB)
    :return: None
    """

    url = channel["url"]
    xbmc.Player().play(url)


def open_ukraina(channel):
    """
    Opens Ukraina channel's live stream
    :param channel: channel to open (from channelsDB)
    :return: None
    """

    url = channel["url"]
    data = urllib2.urlopen(url)
    #html = data.read()
    #debug(html)
    player_found = False
    source_found = False
    stream_url = ""
    stream_found = False
    for line in data:
        if "new DSPlayer(" in line:
            player_found = True
        if player_found:
            if "source:" in line:
                source_found = True
        if source_found:
            start_url = line.find("http://")
            if start_url >= 0:
                stream_found = True
                stream_url = line[start_url:]
                end_url = stream_url.find("',")
                if end_url >= 0:
                    stream_url = stream_url[:end_url]
                break
    if stream_found:
        xbmc.Player().play(stream_url)
    else:
        error(translate(30010))

def get_channel_id_by_username(username):
    """
    Gets ID of youtube channel for given username
    :param username: str - username
    :return: str
    """

    response = youtube_client.get_channel_by_username(username)
    debug(response)
    if response["items"]:
        return response["items"][0]["id"]
    else:
        return ""


def get_live_stream_id(youtube_channel_id):
    """
    Gets id of live video stream from channel with given id
    :param youtube_channel_id: str
    :return: str - id of live video
    """

    params = {"part": "id",
              "channelId": youtube_channel_id,
              "eventType": "live",
              "type": "video"}
    response = youtube_client._perform_v3_request(path="search",
                                                       params=params,
                                                       quota_optimized=False)
    debug(response)
    if response["items"]:
        return response["items"][0]["id"]["videoId"]
    else:
        return ""


def error(message):
    """
    Opens notification window with error message
    :param: message: str - error message
    :return: None
    """
    notify("Error:," + message)


def notify(message):
    """
    Opensa notification window with message
    :param: message: str - message
    :return: None
    """
    icon = os.path.join(addonFolder, "icon.png")
    xbmc.executebuiltin(unicode('XBMC.Notification('+ message +',3000,'+icon+')').encode("utf-8"))


def add_channel_to_menu(id, name, icon):
    """
    Adds channel to the main menu of the plugin
    :param name: - name of channel
    :return: None
    """

    iconImage = image_path(icon)
    listItem = xbmcgui.ListItem(name, iconImage=iconImage)
    # listItem.setProperty("IsPlayable", "true")
    url_data = [("channel_id", id)]
    url = sys.argv[0] + "?" + urllib.urlencode(url_data)
    xbmcplugin.addDirectoryItem(handle=pluginhandle, url=url, listitem=listItem)


def update_channels_db():
    """
    Updates channelsDB
    :rtype : None
    :return: None
    """

    # add_channel_to_db(id="1stnational",
    #                   name=translate(30001),
    #                   icon="1stnational.jpg",
    #                   username="1tvUkraine")
    add_channel_to_db(id="112channel",
                      name=translate(30002),
                      icon="112channel.png",
                      type="youtube",
                      username="",
                      youtube_channel_id="UC-l6fZMH7JLumIR-9o7xrQg")
    add_channel_to_db(id="24channel",
                      name=translate(30003),
                      icon="24channel.png",
                      type="youtube",
                      username="news24ru")
    add_channel_to_db(id="5channel",
                      name=translate(30004),
                      icon="5channel.png",
                      type="youtube",
                      username="5channel")
    add_channel_to_db(id="businesstv",
                      name="Business TV",
                      icon="businesstv.png",
                      type="youtube",
                      username="",
                      youtube_channel_id="UCcnhIV7OAUN8kfgYER9GBUA")
    add_channel_to_db(id="espresotv",
                      name=translate(30005),
                      icon="espresotv.png",
                      type="youtube",
                      username="espresotv")
    add_channel_to_db(id="hromadsketv",
                      name=translate(30006),
                      icon="hromadsketv.jpg",
                      type="youtube",
                      username="HromadskeTV")
    add_channel_to_db(id="ictv",
                      name="ICTV",
                      icon="ictv.png",
                      type="ictv",
                      username="",
                      youtube_channel_id="",
                      video_id="",
                      url="rtmp://stream.ictv.ua:80/live playpath=ictv.stream swfURL=http://ictv.ua/swfobject/zl_player.swf app=live pageURL=http://ictv.ua/ru/index/online")
    add_channel_to_db(id="newsone",
                      name=translate(30008),
                      icon="newsone.jpg",
                      type="youtube",
                      username="",
                      youtube_channel_id="UC9oI0Du20oMOlzsLDTQGfug")
    add_channel_to_db(id="uatv",
                      name="UA|TV",
                      icon="uatv.jpg",
                      type="youtube",
                      username="",
                      youtube_channel_id="UCt3igz3aIXfS108KV_jZsMA")
    add_channel_to_db(id="ukraina",
                      name=translate(30011),
                      icon="ukraina.jpg",
                      type="ukraina",
                      username="",
                      youtube_channel_id="",
                      url="http://kanalukraina.tv/online/")
    add_channel_to_db(id="ukrlifetv",
                      name="UKRLIFE.TV",
                      icon="ukrlifetv.png",
                      type="youtube",
                      username="TVUKRLIFE")
    add_channel_to_db(id="ubr",
                      name=translate(30007),
                      icon="ubr.png",
                      type="youtube",
                      username="",
                      youtube_channel_id="UCw0yOBzjVydRjSVnXVIGt3w")


def add_channel_to_db(id, name,
                      icon,
                      type="youtube",
                      username="",
                      youtube_channel_id="",
                      video_id="",
                      url=""):
    """
    Adds channel to channelsDB
    :param id: id channel's id
    :param name: name of channel (in local language)
    :param icon: filename of channel's logo
    :param type: type of channel ("youtube" or "ictv")
    :param username: YouTube username of channel
    :param youtube_channel_id: id of YouTube channel
    :param video_id: id of live stream of channel
    :param url: url of the stream
    :return: None
    """

    channelsDB[id] = {"name": name,
                      "icon": icon,
                      "type": type,
                      "username": username,
                      "youtube_channel_id": youtube_channel_id,
                      "video_id": video_id,
                      "url": url}


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
    if type(content) is str:
        message = unicode(content, "utf-8")
    else:
        message = content
    log(message, xbmc.LOGDEBUG)

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
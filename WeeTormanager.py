#!/usr/bin/env python2
#-*- coding: utf-8 -*-
#
# WeeTormanager.py - A simple script for weechat for banning all Tor-Exit-Nodes
#
# Copyright (c) 2013 by Christian Rebischke <Chris.Rebischke@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/
#
#======================================================================
# Author: Christian Rebischke alias Shibumi
# Github: https://github.com/shibumi
# Email: Chris.Rebischke@gmail.com
# GPG: E2C0DC2A
#
# Please run this script with ircop axx ;) script is for ircops only
# Please set anti_flood_prio on 0
# /set irc.server.<server>.anti_flood_prio_high 0
# /set irc.server.<server>.anti_flood_prio_low 0
#
# TODO: Use URL-Function
#
#


name="WeeTormanager"
author="Shibumi"
version="1.0"
license="GPL"
description="Bans and unbans all tor exit nodes"
shutdown_function=""
charset=""

try:
  import weechat

except ImportError:
  print("This script must be run under WeeChat.")
  print("Get WeeChat now at: http://www.weechat.org/")
  exit()

try:
  import socks
  import socket
  socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, '127.0.0.1', 9050, True)
  socket.socket = socks.socksocket
  import urllib2

except ImportError:
  print("Please install python-socksipy")
  exit()

def torban(data, buffer, args):
  for ip in urllib2.urlopen("http://torstatus.blutmagie.de/ip_list_exit.php/Tor_ip_list_EXIT.csv").readlines():
    weechat.command("","/quote ZLINE  %s/32 +10d Tor Exit please use oh6ev55uo4cmgh4w.onion to connect" % ip.strip("\n"))
  weechat.prnt("","SUCCESS - Your IRC server will not accept tor-exit-node-users")
  return weechat.WEECHAT_RC_OK

def torunban(data, buffer, args):
  for ip in urllib2.urlopen("http://torstatus.blutmagie.de/ip_list_exit.php/Tor_ip_list_EXIT.csv").readlines():
    weechat.command("","/quote ZLINE  %s/32" % ip.strip("\n"))
  weechat.prnt("","DANGER - Your IRC server will accept tor-exit-node-users")
  return weechat.WEECHAT_RC_OK

if __name__ == "__main__":
  weechat.register(name, author, version, license, description, shutdown_function, charset)
  weechat.hook_command("torban","bans all exitnodes","","","","torban","")
  weechat.hook_command("torunban","unbans all exitnodes","","","","torunban","")

#set ts=2 sts=2 sw=2 et

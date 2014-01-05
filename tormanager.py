#!/usr/bin/env python2
#-*- coding: utf-8 -*-
#
# tormanager.py - A simple xchat script for banning all tor-exitnodes
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
# GitHub: https://github.com/shibumi
# Email : Chris.Rebischke@gmail.com
# GPG: E2C0DC2A
#
# Please set net_throttle on off -> /set net_throttle off
#
__module_name__="tormanager.py"
__module_version__="1.0"
__module_description__="Bans and unbans all tor exit nodes"
__module_author__="Shibumi"

import xchat, urllib2

class tormanager:
	def __init__(self):
		xchat.hook_command("torban",self.torban, help="/torban - bans all tor exit nodes")
		xchat.hook_command("torunban", self.torunban, help="/torunban - unbans all tor exit nodes")
		
		
	def torban(self, word, word_eol, userdata):
		for ip in urllib2.urlopen("http://torstatus.blutmagie.de/ip_list_exit.php/Tor_ip_list_EXIT.csv").readlines():
			xchat.command("ZLINE  %s/32 +10d Tor Exit please use oh6ev55uo4cmgh4w.onion to connect" % ip.strip("\n"))
		print("SUCCESS - Your IRC server will not accept tor-exit-node-users")
		
	def torunban(self, word, word_eol, userdata):
		for ip in urllib2.urlopen("http://torstatus.blutmagie.de/ip_list_exit.php/Tor_ip_list_EXIT.csv").readlines():
			xchat.command("ZLINE  %s/32" % ip.strip("\n"))
		print("DANGER - Your IRC server will accept tor-exit-node-users")
			
			
tormanager()
		

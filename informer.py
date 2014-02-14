#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# informer.py - A simple xchat script for checking joining users
# 
# Copyright (c) 2013 by Christian Rebischke <Q2hyaXMuUmViaXNjaGtlQGdtYWlsLmNvbQo= | base64 -d>
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
# Email : Q2hyaXMuUmViaXNjaGtlQGdtYWlsLmNvbQo= | base64 -d
# GPG: E2C0DC2A
#
# ONLY FOR XCHAT/HEXCHAT(!!)
#
# TODO: Multichannel support
#


import xchat
__module_name__="informer"
__module_version__="1.0"
__module_description__="check joining users!"

####CONFIG######
CHANNEL="#CHANNEL"
#################



class informer(object):
	def __init__(self):
		xchat.hook_print("Join",self.onJoin)
	
	def onJoin(self, word, word_eol, userdata):
		username = word[0]
		if word[1] == CHANNEL:
			xchat.command("ctcp %s version" % username)
			xchat.command("QUOTE whois %s" % username)
		
informer()
		
#set ts=2 sts=2 sw=2 et		
		

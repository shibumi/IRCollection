#!/usr/bin/env python2
#-*- coding: utf-8 -*-
#
# Antiflood.py - A simple xchat script that zlines joining spambots
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


import xchat, re

__module_name__="antiflood"
__module_version__="1.0"
__module_description__="zline joining spambots!"
__module_author__="shibumi"

REGEX="^[A-Za-z]{2}$"
CHANNEL="#germany"


class antiflood(object):
	def __init__(self):
		xchat.hook_print("Join", self.onJoin)
		
	def onJoin(self, word, word_eol, userdata):
		username = word[0]
		pattern = re.compile(REGEX)
		userhost = word[2]
		userhost = userhost.split("@")
		ident = userhost[0]
		chars = len(ident)
		if word[1] == CHANNEL:
			if pattern.match(ident) != None:
				xchat.command("ZLINE %s 10d mess with the best die like the rest" % username)

			
antiflood()

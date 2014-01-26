#!/usr/bin/env python2
#-*- coding: utf-8 -*-
#
# masstransfer.py - A simple xchat script for moving all users from one channel in another
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
# script requires ircop access

__module_name__="masstransfer.py"
__module_version__="1.0"
__module_description__="joins all users from one chan in another chan"
__module_author__="shibumi"

import xchat

class masstransfer:
  def __init__(self):
    xchat.hook_command("masstransfer",self.process, help="/epicjoin <source> <destination> move every user from source to destination")

  def process(self, word, word_eol, userdata):
    partchannel = word[1]
    joinchannel = word[2]
    cnc = xchat.find_context(channel = partchannel)
    for user in cnc.get_list("users"):
      cnc.command("QUOTE sapart %s %s " % (user.nick , partchannel))
      cnc.command("QUOTE sajoin %s %s " % (user.nick , joinchannel))


masstransfer()

#set ts=2 sts=2 sw=2 et

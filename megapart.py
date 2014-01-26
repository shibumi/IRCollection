#!/usr/bin/env python2
#-*- coding: utf-8 -*-
#
# megapart.py - A simple xchat script for isolating one user
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

__module_name__="megapart.py"
__module_version__="1.0"
__module_description__="kicks a user out of every channel"
__module_author__="shibumi"

import xchat


class main(object):
  def __init__(self):
    self.whoishook = None
    self.timer = None
    xchat.hook_command("megapart",self.megapart, help="/logpart <user> kicks a user out of every channel")

  def megapart(self, word, word_eol, userdata):
    self.whoishook = xchat.hook_server("319",self.got_319)
    self.timer = xchat.hook_timer(120000,self.reset)
    user = word[1]
    xchat.command("QUOTE whois %s" % user)

  def got_319(self, word, word_eol, userdata): 
    user = word[3]
    channel = word_eol[4].lstrip(":")
    channel = channel.split(" ")
    print "removing.. %s aus %r" % (user,channel)
    for chan in channel:
      xchat.command("QUOTE sapart %s %s" % (user, chan.lstrip("+%@&~")))
      if self.whoishook:
        xchat.unhook(self.whoishook)
        self.whoishook = None
      if self.timer:
        xchat.unhook(self.timer)
        self.timer = None

      def reset(self, userdata):
        if self.whoishook:
          xchat.unhook(self.whoishook)
          self.whoishook = None
        self.timer = None
        return False

main()

#set ts=2 sts=2 sw=2 et

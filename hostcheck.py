#!/usr/bin/env python2
#-*- coding: utf-8 -*-
#
# hostcheck.py - A simple xchat script for comparing joining hosts
#
# Copyright (c) 2013 by Christian Rebischke <echo Q2hyaXMuUmViaXNjaGtlQGdtYWlsLmNvbQo= | base64 -d>
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
# Email: echo Q2hyaXMuUmViaXNjaGtlQGdtYWlsLmNvbQo= | base64 -d
# GPG: E2C0DC2A
#
# 
#
#
__module_name__="hostcheck"
__module_version__="1.2"
__module_description__="checks and compare hosts"
__module_author__="shibumi"


import xchat

class hostcheck(object):

  def __init__(self):
    xchat.hook_command("hostcheck", self.check_process, help="/hostcheck <channel>")


  def check_process(self, word, word_eol, userdata):
    self.checkchannel = word[1]
    self.hostlist = []
    self.kicklist = []
    xchat.hook_print("Join", self.onJoin)
    xchat.hook_print("Quit", self.onQuit)
    xchat.hook_print("Part", self.onPart)
    xchat.hook_print("Kick", self.onKick)
    xchat.hook_print("Part with Reason", self.onPartReason)
    self.IRCserver = xchat.get_info("server")
    self.cnc = xchat.find_context(channel = self.checkchannel, server= self.IRCserver)
    userlist = self.cnc.get_list("users")
    for i in userlist:
      if i.host not in self.hostlist:
        self.hostlist.append(i.host)
      elif i.host in self.hostlist:
        self.cnc.prnt("\0034\007\002CLONE DETECTED = %s" % i.host)
        #print(self.hostlist) #DEBUG
    print("Script ready")

  def onJoin(self, word, word_eol, userdata):
    #print("DEBUG:", self.checkchannel, word[1], word[2]) #DEBUG
    if self.checkchannel == word[1]:
      userhost = word[2]			
      if word[0] not in self.kicklist:
        if userhost not in self.hostlist:
          self.hostlist.append(userhost)

        elif userhost in self.hostlist:
          #cnc = xchat.find_context(channel = self.checkchannel)
          self.cnc.prnt("\0034\007\002CLONE DETECTED = %s" % userhost)

  def onQuit(self, word, word_eol, userdata):
    if word[0] in self.kicklist:
      self.kicklist.remove(word[0])
    if word[2] in self.hostlist:
      self.hostlist.remove(word[2])

  def onPart(self, word, word_eol, userdata):
    if word[0] in self.kicklist:
      self.kicklist.remove(word[0])
    if word[1] in self.hostlist:
      self.hostlist.remove(word[1])

  def onPartReason(self, word, word_eol, userdata):
    if word[0] in self.kicklist:
      self.kicklist.remove(word[0])
    if word[1] in self.hostlist:
      self.hostlist.remove(word[1])

  def onKick(self, word, word_eol, userdata):
    self.kicklist.append(word[1])	

hostcheck()

#set ts=2 sts=2 sw=2 et



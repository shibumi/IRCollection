#!/usr/bin/env python2
#-*- coding: utf-8 -*-
#
# dbot.py - An IRC-Bot for providing an IRC-Server with restricted Tor-Access
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
#
#
#
# How your database must look like...
# 0|ident|varchar(30)|0||1
# 1|password|varchar(64)|0||0
# 2|locked|bool(1)|0||0
#

###################IMPORTS#####################

import string
import time
import sqlite3

#####################CONFIG SECTION#############

HOST=""
PORT=
NICK=""
CHAN=""
LOGIN=""
OPERLOGIN=""
DATABASE=""
TORSUPPORT=0 #Enable torsupport with 1 ( needs socksipy )

################################################



class ircbot(object):

  def __init__(self):
    self.connection = sqlite3.connect(DATABASE)
    self.c = self.connection.cursor()
    self.readbuffer=""
    if TORSUPPORT == 0:
      import socket
      self.s = socket.socket()
    else:
      import socks
      self.s = socks.socksocket() 
      self.s.setproxy(socks.PROXY_TYPE_SOCKS5,"127.0.0.1",9050) 
    try:
      self.s.connect((HOST, PORT))
    except:
      print "[-] Problem connecting on %s %s" % (HOST, PORT)
      exit(1)

    self.s.send("NICK %s\r\n" % NICK)
    self.s.send("USER %s %s bla :%s\r\n" % (NICK , NICK, NICK))
    time.sleep(5)
    self.s.send("PRIVMSG nickserv :identify %s\r\n" % LOGIN)
    self.s.send("OPER Protector %s\r\n" % OPERLOGIN)
    self.s.send("JOIN %s\r\n" % CHAN)
    self.main()

  def main(self):
    while 1:
      self.readbuffer=self.readbuffer+self.s.recv(1024)
      temp=string.split(self.readbuffer, "\n")
      self.readbuffer=temp.pop()
      for line in temp:
        line=string.rstrip(line)
        line=string.split(line)
        print line
        try:
          if line[3] == ":!torusers" and line[2] == CHAN:
            self.c.execute("SELECT * FROM torusers")
            self.r = self.c.fetchall()
            for row in self.r:
              self.s.send("PRIVMSG %s :%s\r\n" % (CHAN, "%15.15s %60.60s %s" % row ))

          if line[3] == ":!identsearch" and line[2] == CHAN:
            self.c.execute("SELECT * FROM torusers where ident = %s" % "'"+line[4]+"'")
            self.r = self.c.fetchall()
            if self.r == []:
              self.s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] User not found"))
            else:
              self.s.send("PRIVMSG %s :%s\r\n" % (CHAN, self.r))

          if line[3] == ":!torlock" and line[2] == CHAN:
            self.c.execute("UPDATE torusers set locked = 1 where ident = %s" % "'"+line[4]+"'")
            self.c.execute("SELECT * FROM torusers where ident = %s" % "'"+line[4]+"'")
            self.r = self.c.fetchall()
            if self.r == []:
              self.s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] User not found"))
            else:
              self.s.send("PRIVMSG %s :%s\r\n" % (CHAN, self.r))
              self.connection.commit()

          if line[3] == ":!torunlock" and line[2] == CHAN:
            self.c.execute("UPDATE torusers set locked = 0 where ident = %s" % "'"+line[4]+"'")
            self.c.execute("SELECT * FROM torusers where ident = %s" % "'"+line[4]+"'")
            self.r = self.c.fetchall()
            if self.r == []:
              self.s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] User not found"))
            else:
              self.s.send("PRIVMSG %s :%s\r\n" % (CHAN, self.r))
              self.connection.commit()

          if line[3] == ":!toradd" and line[2] == CHAN:
            self.c.execute("SELECT * FROM torusers where ident = %s" % "'"+line[4]+"'")
            self.r = self.c.fetchall()
            if self.r != []:
              self.s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] User exists. Please remove user first."))
            else:
              self.c.execute("INSERT INTO torusers VALUES (%s, %s, 0)" % ( "'"+line[4]+"'","'"+line[5]+"'"))
              self.c.execute("SELECT * FROM torusers where ident = %s" % "'"+line[4]+"'")
              self.r = self.c.fetchall()
              self.s.send("PRIVMSG %s :%s\r\n" % (CHAN, self.r))
              self.s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] Done"))
              self.connection.commit()
    
          if line[3] == ":!tordel" and line[2] == CHAN:
            self.c.execute("SELECT * FROM torusers where ident = %s" % "'"+line[4]+"'")
            self.r = self.c.fetchall()
            if self.r == []:
              self.s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] User does not exist"))
            else:
              self.c.execute("DELETE FROM torusers WHERE ident = %s" % "'"+line[4]+"'")
              self.s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] Done"))
              self.connection.commit()

          if line[3] == ":!help" and line[2] == CHAN:
            self.s.send("PRIVMSG %s :%s\r\n" % (CHAN ,"[+] ++++++++++Help menu+++++++++++++"))
            self.s.send("PRIVMSG %s :%s\r\n" % (CHAN ,"[+] !torusers - list all tor-users"))
            self.s.send("PRIVMSG %s :%s\r\n" % (CHAN ,"[+] !torsearch - search for for ident"))
            self.s.send("PRIVMSG %s :%s\r\n" % (CHAN ,"[+] !torlock - lock tor-access"))
            self.s.send("PRIVMSG %s :%s\r\n" % (CHAN ,"[+] !torunlock - unlock tor-access"))
            self.s.send("PRIVMSG %s :%s\r\n" % (CHAN ,"[+] !toradd - add user to db"))
            self.s.send("PRIVMSG %s :%s\r\n" % (CHAN ,"[+] !tordel - remove user from db"))


        except(IndexError):
          pass

        if(line[0]=="PING"):
          self.s.send("PONG %s\r\n" % line[1])

ircbot()


#set ts=2 sts=2 sw=2 et

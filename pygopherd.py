#!/usr/bin/python2.2

# Python-based gopher server
# COPYRIGHT #
# Copyright (C) 2002 John Goerzen
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# END OF COPYRIGHT #

#

from ConfigParser import ConfigParser
import socket, os, sys, SocketServer
from pygopherd import handlers, protocols
from pygopherd.protocols import ProtocolMultiplexer
import mimetypes

config = ConfigParser()
config.read("pygopherd.conf")
mimetypes.init([config.get("pygopherd", "mimetypes")])

class GopherRequestHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        request = self.rfile.readline()

        protohandler = \
                     ProtocolMultiplexer.getProtocol(request, \
                     self.server, self, self.rfile, self.wfile, self.server.config)
        protohandler.handle()

class MyServer(SocketServer.ForkingTCPServer):
    allow_reuse_address = 1

    def server_bind(self):
        """Override server_bind to store server name."""
        SocketServer.ForkingTCPServer.server_bind(self)
        host, port = self.socket.getsockname()
        self.server_name = socket.getfqdn(host)
        self.server_port = port
        

s = MyServer(('', config.getint('pygopherd', 'port')),
             GopherRequestHandler)
s.config = config
s.serve_forever()


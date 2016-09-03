"""Foghornc --- Foghorn client for RPC"""

import httplib
import socket
import xmlrpclib
import sys

class UnixStreamHTTPConnection(httplib.HTTPConnection):
    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(self.host)


class UnixStreamTransport(xmlrpclib.Transport, object):
    def __init__(self, socket_path):
        self.socket_path = socket_path
        super(UnixStreamTransport, self).__init__()

    def make_connection(self, host):
        return UnixStreamHTTPConnection(self.socket_path)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        sys.argv.append(None)
    if len(sys.argv) != 4:
        print "foghornc.py [command] [arg] <arg2>"
        exit(1)
    (_, command, arg, arg2) = sys.argv
    server = xmlrpclib.Server('http://arg_unused',
                              transport=UnixStreamTransport("foghornd.sock"),
                              allow_none=1)

    functions = {
        "add_to_whitelist": lambda arg: server.add_to_whitelist(arg, arg2),
        "add_to_blacklist": lambda arg: server.add_to_blacklist(arg, arg2),
        "add_to_greylist": lambda arg: server.add_to_greylist(arg, arg2),

        "delete_from_whitelist": lambda arg: server.delete_from_whitelist(arg),
        "delete_from_blacklist": lambda arg: server.delete_from_blacklist(arg),
        "delete_from_greylist": lambda arg: server.delete_from_greylist(arg),

        "delete_tag_from_whitelist": lambda arg: server.delete_tag_from_whitelist(arg),
        "delete_tag_from_blacklist": lambda arg: server.delete_tag_from_blacklist(arg),
        "delete_tag_from_greylist": lambda arg: server.delete_tag_from_greylist(arg),
    }

    if command in functions.keys():
        functions[command](arg)
    else:
        print "Unkown command: %s" % command

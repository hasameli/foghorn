"""Foghornc --- Foghorn client for RPC"""

import httplib
import socket
import xmlrpclib
import sys


class UnixStreamHTTPConnection(httplib.HTTPConnection):
    """Connect socket"""
    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(self.host)


class UnixStreamTransport(xmlrpclib.Transport, object):
    """Connect HTTP to Unix Socket"""
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
    (_, COMMAND, ARG, ARG2) = sys.argv
    SERVER = xmlrpclib.Server('http://arg_unused',
                              transport=UnixStreamTransport("foghornd.sock"),
                              allow_none=1)

    FUNCTIONS = {
        "query_host": lambda: SERVER.query_host(ARG),

        "add_to_whitelist": lambda: SERVER.add_to_whitelist(ARG, ARG2),
        "add_to_blacklist": lambda: SERVER.add_to_blacklist(ARG, ARG2),
        "add_to_greylist": lambda: SERVER.add_to_greylist(ARG, ARG2),

        "delete_from_whitelist": lambda: SERVER.delete_from_whitelist(ARG),
        "delete_from_blacklist": lambda: SERVER.delete_from_blacklist(ARG),
        "delete_from_greylist": lambda: SERVER.delete_from_greylist(ARG),

        "delete_tag_from_whitelist": lambda: SERVER.delete_tag_from_whitelist(ARG),
        "delete_tag_from_blacklist": lambda: SERVER.delete_tag_from_blacklist(ARG),
        "delete_tag_from_greylist": lambda: SERVER.delete_tag_from_greylist(ARG),
    }

    if COMMAND in FUNCTIONS.keys():
        RESULT = FUNCTIONS[COMMAND]()
        print "Result: %s" % RESULT
    else:
        print "Unkown command: %s" % COMMAND

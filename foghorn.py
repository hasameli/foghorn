#!/usr/bin/env python

'''
    Launches the Foghorn daemon.

    :copyright: (c) 2016 by Eric Rand and Nik LaBelle
    :license: MIT, see docs/LICENSING for more details.
'''

from foghornd import Main

if __name__ == '__main__':
    foghornd = Main()
    foghornd.run()

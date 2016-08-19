#!/usr/bin/env python

'''
    Launches the Foghorn twisted daemon.

    :copyright: (c) 2016 by Eric Rand and Nik LaBelle
    :license: MIT, see docs/LICENSING for more details.
'''

import subprocess

if __name__ == '__main__':
    proc = subprocess.Popen(["twistd", "-ny", "foghornd.tac"], shell=False)
    proc.wait()

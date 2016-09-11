#!/usr/bin/env python

'''
    Packing for Foghorn.

    :copyright: (c) 2016 by Eric Rand and Nik LaBelle
    :license: MIT, see docs/LICENSING for more details.
'''

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


# SETTINGS
# --------

DEPENDENCIES = [
    'twisted'
]

SHORT_DESCRIPTION = 'Foghorn is a configurable DNS proxy to allow for black-, white-, and greylisting of DNS resources.'

LONG_DESCRIPTION = '''Foghorn is a configurable DNS proxy to allow for
black-, white-, and greylisting of DNS resources.

foghorn MUST be positioned within a network with egress filtering enabled
for DNS - only the local resolver can be allowed to make outbound requests
for DNS.

Also, squid or some similar proxy should be in place to filter naked
IP requests, in order to mitigate the possibility of certain workarounds
that would otherwise be available to attackers.

After baselining, the workstations that you desire to protect should be
configured to use the foghorn server as their DNS resolver, and any ACLs
adjusted accordingly.
'''

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Information Technology',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Topic :: Security',
    'Topic :: System :: Networking :: Monitoring',
    'Operating System :: Unix',
    'Operating System :: POSIX :: Linux',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
]

# SETUP
# -----

setup(name='Foghorn',
      version="0.0.1",
      description=SHORT_DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author="Eric Rand",
      author_email="foghorn@hasameli.com",
      maintainer="Eric Rand",
      maintainer_email="foghorn@hasameli.com",
      packages=['foghornd'],
      package_data={'foghornd': [
          'plugins/*.py',
          'plugins/listhandler/*',
          'plugins/logger/*',
          'greydns/*',
          'settings.json'
      ]},
      scripts=['foghorn.py', 'foghornd.tac'],
      include_package_data=True,
      install_requires=DEPENDENCIES,
      setup_requires=DEPENDENCIES,
      zip_safe=False)

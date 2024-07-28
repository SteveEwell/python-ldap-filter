"""
python-ldap-filter
==================

**Build and generate LDAP filters**

A Python utility library for working with Lightweight Directory Access
Protocol (LDAP) filters.

This project is a port of the
`node-ldap-filters <https://github.com/tapmodo/node-ldap-filters>`__ and
implements many of the same APIs. The filters produced by the library
are based on `RFC 4515 <https://tools.ietf.org/html/rfc4515>`__.

Links
-----

`GitHub <https://github.com/SteveEwell/python-ldap-filter>`_

"""

import os
import sys
from setuptools import setup

if sys.version_info[0] <= 2 or (sys.version_info[0] == 3 and sys.version_info < (3, 4)):
    raise RuntimeError('This software requires Python version 3.4 or higher.')

if os.path.isfile("MANIFEST"):
    os.unlink("MANIFEST")

rootdir = os.path.dirname(__file__) or "."


setup()

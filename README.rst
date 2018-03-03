python-ldap-filter
==================

**Build and generate LDAP filters**

.. image:: https://img.shields.io/pypi/v/ldap-filter.svg
    :target: https://pypi.python.org/pypi/ldap-filter/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/l/ldap-filter.svg
    :target: https://pypi.python.org/pypi/ldap-filter/
    :alt: License

.. image:: https://img.shields.io/travis/SteveEwell/python-ldap-filter/master.svg
    :target: https://travis-ci.org/SteveEwell/python-ldap-filter
    :alt: TRAVIS-CI build status for master branch

.. image:: https://img.shields.io/coveralls/github/SteveEwell/python-ldap-filter/master.svg
    :target: https://coveralls.io/github/SteveEwell/python-ldap-filter
    :alt: Coveralls code coverage for master branch


A Python utility library for working with Lightweight Directory Access
Protocol (LDAP) filters.

This project is a port of the
`node-ldap-filters <https://github.com/tapmodo/node-ldap-filters>`__ and
implements many of the same APIs. The filters produced by the library
are based on `RFC 4515 <https://tools.ietf.org/html/rfc4515>`__.

Usage
=====

Installation
------------

Install via pip:

.. code:: bash

    pip install ldap-filter

Building a Filter
-----------------

.. code:: python

    from ldap_filter import Filter

    output = Filter.AND([
        Filter.attribute('givenName').equal_to('bob'),
        Filter.attribute('mail').ends_with('@example.com')
    ])

    print(output.to_string())  # (&(givenName=bob)(mail=*@example.com))
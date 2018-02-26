python-ldap-filter
==================

**Build and generate LDAP filters**

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

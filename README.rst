Python LDAP Filter · |Latest Version| |License| |TRAVIS-CI build status for master branch| |Coveralls code coverage for master branch|
======================================================================================================================================

    Build, generate, and validate LDAP filters

A Python 3 utility library for working with Lightweight Directory Access
Protocol (LDAP) filters.

This project is a Python port of the
`node-ldap-filters <https://github.com/tapmodo/node-ldap-filters>`__
project. The filters produced by the library are based on `RFC
4515 <https://tools.ietf.org/html/rfc4515>`__.

**Note:** This project is currently only compatible with Python 3.4 or
higher.

Usage
=====

Installation
------------

Install via pip:

.. code:: bash

    pip install ldap-filter

Building a Filter
-----------------

This library exposes a number of APIs that allow you to build filters
programmatically. The logical and attribute methods of the ``Filter``
object can be combined in a number of ways to generate filters ranging
from very simple to very complex.

The following is a quick example of how you might build a filter
programmatically:

.. code:: python

    from ldap_filter import Filter

    output = Filter.AND([
        Filter.attribute('name').equal_to('bob'),
        Filter.attribute('mail').ends_with('@example.com'),
        Filter.OR([
            Filter.attribute('dept').equal_to('accounting'),
            Filter.attribute('dept').equal_to('operations')
        ])
    ])

    print(output.to_string())  # (&(name=bob)(mail=*@example.com)(|(dept=accounting)(dept=operations)))

Attribute Methods
~~~~~~~~~~~~~~~~~

Attribute methods are used to create LDAP attribute filter strings. The
``Filter.attribute(name)`` method returns an ``Attribute`` object that
the following filter methods can be applied to.

.. code:: python

    output = Filter.attribute('name').equal_to('bob')  # (name=bob)

Methods:
^^^^^^^^

-  **Attribute.present()** - Tests if an attribute is present.

   -  *Output:* ``(attribute=*)``

-  **Attribute.equal_to(value)** - Tests if an attribute is equal to the
   provided ``value``.

   -  *Output:* ``(attribute=value)``

-  **Attribute.contains(value)** - Tests if an attribute contains the
   provided ``value``.

   -  *Output:* ``(attribute=*value*)``

-  **Attribute.starts_with(value)** - Tests if an attribute starts with
   the provided ``value``.

   -  *Output:* ``(attribute=value*)``

-  **Attribute.ends_with(value)** - Tests if an attribute ends with the
   provided ``value``.

   -  *Output:* ``(attribute=*value)``

-  **Attribute.approx(value)** - Tests if an attribute is an approximate
   match to the provided ``value``.

   -  *Output:* ``(attribute~=value)``

-  **Attribute.gte(value)** - Tests if an attribute is greater than or
   equal to the provided ``value``.

   -  *Output:* ``(attribute>=value)``

-  **Attribute.lte(value)** - Tests if an attribute is less than or
   equal to the provided ``value``.

   -  *Output:* ``(attribute<=value)``

-  **Attribute.raw(value)** - Allows for a custom filter with escaped
   ``value`` output.

   -  *Output:* ``(attribute=value)``

Logical Methods
~~~~~~~~~~~~~~~

Logical methods are used to aggregate simple attribute filters. You can
nest as many logical methods as needed to produce complex filters.

.. code:: python

    output = Filter.OR([
        Filter.attribute('name').equal_to('bob'),
        Filter.attribute('name').equal_to('bill')
    ])

    print(output)  # (|(name=bob)(name=bill))

.. _methods-1:

Methods:
^^^^^^^^

-  **Filter.AND(filt)** - Accepts a list of ``Filter``, ``Attribute``,
   or ``Group`` objects.

   -  *Output:* ``(&(filt=1)(filt=2)..)``

-  **Filter.OR(filt)** - Accepts a list of ``Filter``, ``Attribute``, or
   ``Group`` objects.

   -  *Output:* ``(|(filt=1)(filt=2)..)``

-  **Filter.NOT(filt)** - Accepts a single ``Attribute`` object.

   -  *Output:* ``(!(filt=1))``

Filter Parsing
--------------

The ``Filter.parse(input)`` method can be used to create a ``Filter``
object from an existing LDAP filter. This method can also be used to
determine if a string is a valid LDAP filter or not.

.. code:: python

    input = '(|(name=bob)(name=bill))'

    Filter.parse(input)

If an invalid LDAP filter string is passed a ``ParseError`` exception
will be thrown.

.. code:: python

    from ldap_filter import Filter, ParseError


    input = '(|(name=bob)name=bill))'

    try:
        Filter.parse(input)
    except ParseError as e:
        print(e)

*Error Output:*

::

    Line 1: expected [\x20], [\x09], "\r\n", "\n", '(', ')'
    (|(name=bob)name=bill)
                ^

Simplifying Filters
-------------------

The ``Filter.simplify()`` method can be used to eliminate unnecessary
AND/OR filters that only have one child node.

.. code:: python

    input = '(&(name=bob))'
    complex = Filter.parse(input)

    print(complex.simplify())  # (name=bob)

Filter Output
-------------

There are a few options for getting a string output from your ``Filter``
object with optional custom formatting.

Simple String
~~~~~~~~~~~~~

You can get simple filter string by calling the ``Filter.to_string()``
method. The ``Filter`` class also implements Python’s ``__str__``
method, allowing you to type cast the ``Filter`` object directly to a
string or concatenate with other strings.

.. code:: python

    output = Filter.AND([
        Filter.attribute('name').equal_to('bob'),
        Filter.attribute('mail').ends_with('@example.com'),
    ])

    # Filter.to_string() output.
    print(output.to_string())  # (&(name=bob)(mail=*@example.com))

    # Typecast output.
    print(str(output)) # (&(name=bob)(mail=*@example.com))

    # String concatenate output
    print('LDAP Filter: ' + output) # LDAP Filter: (&(name=bob)(mail=*@example.com))

Beautified String
~~~~~~~~~~~~~~~~~

The ``Filter.to_string()`` method provides additional formatting options
to produce beautified filter strings.

You can get the default beautified format by passing ``True`` to the
``Filter.to_string(indent)`` method

.. code:: python

    output = Filter.AND([
        Filter.attribute('name').equal_to('bob'),
        Filter.attribute('mail').ends_with('@example.com'),
        Filter.OR([
            Filter.attribute('dept').equal_to('accounting'),
            Filter.attribute('dept').equal_to('operations')
        ])
    ])

    print(output.to_string(True))

*Default Beautified Output:*

::

    (&
        (name=bob)
        (mail=*@example.com)
        (|
            (dept=accounting)
            (dept=operations)
        )
    )

or you can customize the output by passing the ``indent`` and/or
``indt_char`` parameters to ``Filter.to_string(indent, indt_char)``. The
``indent`` parameter accepts an integer value while the ``indt_char``
parameter accepts any string or character value.

.. code:: python

    output = Filter.AND([
        Filter.attribute('name').equal_to('bob'),
        Filter.attribute('mail').ends_with('@example.com'),
        Filter.OR([
            Filter.attribute('dept').equal_to('accounting'),
            Filter.attribute('dept').equal_to('operations')
        ])
    ])

    print(output.to_string(2, '.'))

*Custom Beautified Output:*

::

    (&
    ..(name=bob)
    ..(mail=*@example.com)
    ..(|
    ....(dept=accounting)
    ....(dept=operations)
    ..)
    )

Filter Matching
---------------

The ``Filter.match(data)`` method allows you to evaluate a Python
dictionary with attributes against an LDAP filter. The method will
return ``True`` if a match is found or ``False`` if there is no match
(or if an attribute matches a **NOT** exclusion).

.. code:: python

    filt = Filter.AND([
        Filter.attribute('department').equal_to('accounting'),
        Filter.NOT(
            Filter.attribute('status').equal_to('terminated')
        )
    ])

    employee1 = {
        'name': 'Bob Smith',
        'department': 'Accounting',
        'status': 'Active'
    }

    print(filt.match(employee1))  # True

    employee2 = {
        'name': 'Jane Brown',
        'department': 'Accounting',
        'status': 'Terminated'
    }

    print(filt.match(employee2))  # False

    employee3 = {
        'name': 'Bob Smith',
        'department': 'Marketing',
        'status': 'Active'
    }

    print(filt.match(employee3))  # False

Unit Tests
==========

In order to run the test suite the pytest library is required. You can
install pytest by running:

.. code:: bash

    pip install pytest

To run the unit tests simply type ``pytest`` in the projects root
directory

Home Page
=========

Project home page is https://github.com/SteveEwell/python-ldap-filter

License
=======

The **Python LDAP Filter** project is open source software released
under the `MIT licence <https://en.wikipedia.org/wiki/MIT_License>`__.
Copyright 2018 Stephen Ewell

.. |Latest Version| image:: https://img.shields.io/pypi/v/ldap-filter.svg
   :target: https://pypi.python.org/pypi/ldap-filter
.. |License| image:: https://img.shields.io/pypi/l/ldap-filter.svg
   :target: https://pypi.python.org/pypi/ldap-filter
.. |TRAVIS-CI build status for master branch| image:: https://img.shields.io/travis/SteveEwell/python-ldap-filter/master.svg
   :target: https://travis-ci.org/SteveEwell/python-ldap-filter
.. |Coveralls code coverage for master branch| image:: https://img.shields.io/coveralls/github/SteveEwell/python-ldap-filter/master.svg
   :target: https://coveralls.io/github/SteveEwell/python-ldap-filter

import pytest
from ldap_filter import Filter


class TestFilterMatch:
    def test_equality(self):
        filt = Filter.attribute('sn').equal_to('smith')
        assert filt.match({'sn': 'smith'})
        assert filt.match({'sn': 'SMITH'})
        assert not filt.match({'sn': 'bob'})

    def test_multi_value_equality(self):
        filt = Filter.attribute('sn').equal_to('smith')
        data = {'sn': ['Sam', 'Smith', 'Swanson', 'Samson']}
        assert filt.match(data)
        data = {'sn': ['Sam', 'Swanson', 'Samson']}
        assert not filt.match(data)

    def test_present(self):
        filt = Filter.attribute('sn').present()
        assert filt.match({'sn': 'smith'})
        assert filt.match({'sn': 'alex'})
        assert not filt.match({'mail': 'smith'})

    def test_present_parsed(self):
        filt = Filter.parse('(sn=*)')
        assert filt.match({'sn': 'smith'})
        assert filt.match({'sn': 'alex'})
        assert not filt.match({'mail': 'smith'})

    def test_contains(self):
        filt = Filter.attribute('sn').contains('smith')
        assert filt.match({'sn': 'smith'})
        assert filt.match({'sn': 'smith-jonson'})
        assert filt.match({'sn': 'jonson-smith'})
        assert filt.match({'sn': 'Von Ubersmith'})
        assert not filt.match({'sn': 'Jonson'})

    def test_starts_with(self):
        filt = Filter.attribute('sn').starts_with('smith')
        assert filt.match({'sn': 'smith'})
        assert filt.match({'sn': 'smith-jonson'})
        assert not filt.match({'sn': 'Von Ubersmith'})

    def test_ends_with(self):
        filt = Filter.attribute('sn').ends_with('smith')
        assert filt.match({'sn': 'smith'})
        assert filt.match({'sn': 'Von Ubersmith'})
        assert not filt.match({'sn': 'smith-jonson'})

    def test_greater_than_numeric(self):
        filt = Filter.attribute('age').gte('10')
        assert filt.match({'age': 10})
        assert filt.match({'age': '10'})
        assert filt.match({'age': 11})
        assert filt.match({'age': '11'})
        assert not filt.match({'age': 9})
        assert not filt.match({'age': '9'})

    def test_greater_than_lexical(self):
        filt = Filter.attribute('name').gte('bob')
        assert filt.match({'name': 'bob'})
        assert filt.match({'name': 'cell'})
        assert not filt.match({'name': 'acme'})

    def test_less_than_numeric(self):
        filt = Filter.attribute('age').lte('10')
        assert filt.match({'age': 9})
        assert filt.match({'age': '9'})
        assert filt.match({'age': 10})
        assert filt.match({'age': '10'})
        assert not filt.match({'age': 11})
        assert not filt.match({'age': '11'})

    def test_less_than_lexical(self):
        filt = Filter.attribute('name').lte('bob')
        assert filt.match({'name': 'acme'})
        assert filt.match({'name': 'bob'})
        assert not filt.match({'name': 'cell'})

    def test_approx(self):
        filt = Filter.attribute('name').approx('ashcroft')
        assert filt.match({'name': 'Ashcroft'})
        assert filt.match({'name': 'Ashcraft'})
        assert not filt.match({'name': 'Ashsoft'})

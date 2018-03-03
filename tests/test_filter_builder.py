import pytest
from ldap_filter import Filter


class TestFilterAttributes:
    def test_present(self):
        filt = Filter.attribute('attr').present()
        string = filt.to_string()
        assert string == '(attr=*)'

    def test_equal_to(self):
        filt = Filter.attribute('attr').equal_to('value')
        string = filt.to_string()
        assert string == '(attr=value)'

    def test_contains(self):
        filt = Filter.attribute('attr').contains('value')
        string = filt.to_string()
        assert string == '(attr=*value*)'

    def test_starts_with(self):
        filt = Filter.attribute('attr').starts_with('value')
        string = filt.to_string()
        assert string == '(attr=value*)'

    def test_ends_with(self):
        filt = Filter.attribute('attr').ends_with('value')
        string = filt.to_string()
        assert string == '(attr=*value)'

    def test_approx(self):
        filt = Filter.attribute('attr').approx('value')
        string = filt.to_string()
        assert string == '(attr~=value)'

    def test_greater_than(self):
        filt = Filter.attribute('attr').gte('value')
        string = filt.to_string()
        assert string == '(attr>=value)'

    def test_lesser_than(self):
        filt = Filter.attribute('attr').lte('value')
        string = filt.to_string()
        assert string == '(attr<=value)'

    def test_raw(self):
        filt = Filter.attribute('attr').raw('value*value')
        string = filt.to_string()
        assert string == '(attr=value*value)'


class TestFilterEscapes:
    def test_escape(self):
        string = Filter.escape('a * (complex) \\value')
        assert string == 'a \\2a \\28complex\\29 \\5cvalue'

    def test_unescape(self):
        string = Filter.unescape('a \\2a \\28complex\\29 \\5cvalue')
        assert string == 'a * (complex) \\value'

    def test_filter_escape(self):
        filt = Filter.attribute('escaped').equal_to('a * (complex) \\value')
        string = filt.to_string()
        assert string == '(escaped=a \\2a \\28complex\\29 \\5cvalue)'

    def test_filter_convert_int(self):
        filt = Filter.attribute('number').equal_to(1000)
        string = filt.to_string()
        assert string == '(number=1000)'

    def test_filter_convert_float(self):
        filt = Filter.attribute('number').equal_to(10.26)
        string = filt.to_string()
        assert string == '(number=10.26)'

    def test_filter_convert_negative(self):
        filt = Filter.attribute('number').equal_to(-10)
        string = filt.to_string()
        assert string == '(number=-10)'


class TestFilterAggregates:
    def test_and_aggregate(self):
        filt = Filter.AND([
            Filter.attribute('givenName').equal_to('bilbo'),
            Filter.attribute('sn').equal_to('baggens')
        ])
        string = filt.to_string()
        assert string == '(&(givenName=bilbo)(sn=baggens))'

    def test_or_aggregate(self):
        filt = Filter.OR([
            Filter.attribute('givenName').equal_to('bilbo'),
            Filter.attribute('sn').equal_to('baggens')
        ])
        string = filt.to_string()
        assert string == '(|(givenName=bilbo)(sn=baggens))'

    def test_not_aggregate(self):
        filt = Filter.NOT([
            Filter.attribute('givenName').equal_to('bilbo')
        ])
        string = filt.to_string()
        assert string == '(!(givenName=bilbo))'

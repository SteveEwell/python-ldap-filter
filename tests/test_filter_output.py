import pytest
from ldap_filter import Filter


class TestFilterOutput:
    def test_to_string(self):
        filt = '(&(|(sn=ron)(sn=bob))(mail=*)(!(account=disabled)))'
        parsed = Filter.parse(filt)
        string = parsed.to_string()
        assert string == filt

    def test_string_typecast(self):
        filt = '(&(|(sn=ron)(sn=bob))(mail=*)(!(account=disabled)))'
        string = str(Filter.parse(filt))
        assert string == filt

    def test_to_simple_concat(self):
        filt = '(&(|(sn=ron)(sn=bob))(mail=*)(!(account=disabled)))'
        string = Filter.parse(filt) + ''
        assert string == filt

    def test_to_complex_concat(self):
        filt = '(&(sn=ron)(sn=bob))'
        string = Filter.parse(filt) + 'test'
        assert string == '(&(sn=ron)(sn=bob))test'


class TestFilterFormatting:
    def test_default_beautify(self):
        filt = '(&(|(sn=ron)(sn=bob))(mail=*))'
        parsed = Filter.parse(filt)
        string = parsed.to_string(True)
        assert string == '(&\n    (|\n        (sn=ron)\n        (sn=bob)\n    )\n    (mail=*)\n)'

    def test_custom_indent_beautify(self):
        filt = '(&(|(sn=ron)(sn=bob))(mail=*))'
        parsed = Filter.parse(filt)
        string = parsed.to_string(2)
        assert string == '(&\n  (|\n    (sn=ron)\n    (sn=bob)\n  )\n  (mail=*)\n)'

    def test_custom_indent_char_beautify(self):
        filt = '(&(|(sn=ron)(sn=bob))(mail=*))'
        parsed = Filter.parse(filt)
        string = parsed.to_string(indent=2, indt_char='!')
        assert string == '(&\n!!(|\n!!!!(sn=ron)\n!!!!(sn=bob)\n!!)\n!!(mail=*)\n)'


class TestFilterSimplify:
    def test_optimized_filter(self):
        filt = '(&(|(sn=ron)(sn=bob))(mail=*)(!(account=disabled)))'
        parsed = Filter.parse(filt)
        string = parsed.simplify().to_string()
        assert string == filt

    def test_unoptimized_filter(self):
        filt = '(&(|(sn=ron)(&(sn=bob)))(|(mail=*))(!(account=disabled)))'
        optimized = '(&(|(sn=ron)(sn=bob))(mail=*)(!(account=disabled)))'
        parsed = Filter.parse(filt)
        string = parsed.simplify().to_string()
        assert string == optimized

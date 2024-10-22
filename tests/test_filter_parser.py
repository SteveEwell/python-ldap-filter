import pytest
from ldap_filter import Filter, ParseError


class TestFilterParser:
    def test_simple_filter(self):
        filt = '(sn=ron)'
        parsed = Filter.parse(filt)
        string = parsed.to_string()
        assert string == filt

    def test_complex_filter(self):
        filt = '(&(|(sn=ron)(sn=bob))(mail=*)(!(account=disabled)))'
        parsed = Filter.parse(filt)
        string = parsed.to_string()
        assert string == filt

    def test_negative_group_filter(self):
        filt = "(!(|(cn=admins)))"
        parsed = Filter.parse(filt)
        assert parsed is not None
        filt = '(&(!(|(sn=ron)(sn=bob)))(mail=*)(|(cn=john)(cn=alex)(cn=rob)))'
        parsed = Filter.parse(filt)
        string = parsed.to_string()
        assert string == filt

    def test_allows_whitespace(self):
        filt = ' (&  (sn=smith with spaces)(one-two<=morespaces) (objectType=object Type) \n )  '
        parsed = Filter.parse(filt)
        string = parsed.to_string()
        assert string == '(&(sn=smith with spaces)(one-two<=morespaces)(objectType=object Type))'

    def test_allows_value_with_exclamation(self):
        filt = '(&(name=Test!)(mail=*@example.com)(|(dept=accounting)(dept=operations)))'
        parsed = Filter.parse(filt)
        test = {'name': 'Test!', 'mail': 'ron@example.com', 'dept': 'operations'}
        assert parsed.match(test)
        test_fail = {'name': 'Test', 'mail': 'ron@example.com', 'dept': 'operations'}
        assert not parsed.match(test_fail)

    def test_allowed_characters(self):
        filt = '(orgUnit=%)'
        parsed = Filter.parse(filt)
        string = parsed.to_string()
        assert string == filt

    def test_oid_attributes(self):
        filt = '(1.3.6.1.4.1.1466.115.121.1.38=picture)'
        parsed = Filter.parse(filt)
        string = parsed.to_string()
        assert string == filt

    def test_escaped_values(self):
        filt = '(o=Parens R Us \\28for all your parenthetical needs\\29)'
        parsed = Filter.parse(filt)
        string = parsed.to_string()
        assert string == '(o=Parens R Us (for all your parenthetical needs))'

    def test_substring_match(self):
        filt = '(sn=*sammy*)'
        parsed = Filter.parse(filt)
        assert getattr(parsed, 'type') == 'filter'
        assert getattr(parsed, 'comp') == '='
        assert getattr(parsed, 'attr') == 'sn'
        assert getattr(parsed, 'val') == '*sammy*'

    def test_no_parenthesis(self):
        filt = 'sn=ron'
        parsed = Filter.parse(filt)
        string = parsed.to_string()
        assert string == '(sn=ron)'

    def test_allows_whitespace_no_parenthesis(self):
        filt = ' \n sn=ron '
        parsed = Filter.parse(filt)
        string = parsed.to_string()
        assert string == '(sn=ron)'

    def test_parser_matching(self):
        filt = '(&(|(sn=ron)(sn=bob))(mail=*))'
        parsed = Filter.parse(filt)
        test = {'sn': 'ron', 'mail': 'ron@example.com'}
        assert parsed.match(test)
        test_fail = {'sn': 'ron'}
        assert not parsed.match(test_fail)

    def test_simple_malformed_error(self):
        with pytest.raises(ParseError):
            filt = '(sn=sammy'
            Filter.parse(filt)

    def test_complex_malformed_error(self):
        with pytest.raises(ParseError):
            filt = '(&(orgUnit=accounting))\n(mail=ron@example.com) f'
            Filter.parse(filt)


import re


class LDAPBase:
    indent = 4
    collapsed = False
    filters = None

    def simplify(self):
        if self.filters:
            if len(self.filters) == 1:
                return self.filters[0].simplify()
            else:
                self.filters = list(map(lambda x: x.simplify(), self.filters))

        return self

    def to_string(self, indent, level, id_char):
        raise NotImplementedError

    def match(self, data):
        raise NotImplementedError

    @staticmethod
    def _indent(indent, level=0, id_char=' '):
        if type(indent) == bool and indent:
            indent = LDAPBase.indent
        else:
            try:
                indent = int(indent)
            except ValueError:
                return ''

        return id_char * (level * indent)

    @staticmethod
    def escape(data):
        escaped = data.replace('\\', '\\5c')
        escaped = escaped.replace('*', '\\2a')
        escaped = escaped.replace('(', '\\28')
        escaped = escaped.replace(')', '\\29')
        escaped = escaped.replace('\x00', '\\00')

        return escaped

    @staticmethod
    def unescape(data):
        unescaped = data.replace('\\5c', '\\')
        unescaped = unescaped.replace('\\2a', '*')
        unescaped = unescaped.replace('\\28', '(')
        unescaped = unescaped.replace('\\29', ')')
        unescaped = unescaped.replace('\\00', '\x00')

        return unescaped

    @staticmethod
    def match_string(data, filt):
        match = _as_list(data)
        if '*' not in filt:
            return any(_ms_helper(m, filt) for m in match)

        return Filter.match_substring(data, filt)

    @staticmethod
    def match_substring(data, filt):
        match = _as_list(data)

        return any(_ss_helper(m, filt) for m in match)

    @staticmethod
    def match_approx(data, filt):  # TODO: Implement LDAPBase.match_approx()
        pass

    @staticmethod
    def match_lte(data, filt):
        match = _as_list(data)

        return any(_lte_helper(m, filt) for m in match)

    @staticmethod
    def match_gte(data, filt):
        match = _as_list(data)

        return any(_gte_helper(m, filt) for m in match)

    @staticmethod
    def AND(filt):
        return GroupAnd(filt)

    @staticmethod
    def OR(filt):
        return GroupOr(filt)

    @staticmethod
    def NOT(filt):
        filt = _as_list(filt)
        if not len(filt) == 1:  # TODO: Error code here.
            raise Exception

        return GroupNot(filt)


class Filter(LDAPBase):
    def __init__(self, attr, comp, val):
        self.type = 'filter'
        self.attr = attr
        self.comp = comp
        self.val = val

    def __repr__(self):
        return 'Filter: %s' % self.to_string()

    def match(self, data):
        value = self.val

        try:
            attrval = data[self.attr]
        except KeyError:
            return False

        if self.comp == '=':
            if value == '*' and attrval:
                return True
            else:
                return Filter.match_string(attrval, value)
        elif self.comp == '<=':
            return Filter.match_lte(attrval, value)
        elif self.comp == '>=':
            return Filter.match_gte(attrval, value)
        elif self.comp == '~=':
            return Filter.match_approx(attrval, value)
        else:
            pass

    def to_string(self, indent=False, level=0, id_char=' '):
        return ''.join([
            self._indent(indent, level, id_char),
            '(',
            self.attr,
            self.comp,
            self.val,
            ')'
        ])

    @staticmethod
    def attribute(name):
        return Attribute(name)


class Group(LDAPBase):
    def __init__(self, comp, filters):
        self.type = 'group'
        self.comp = comp
        self.filters = filters

    def __repr__(self):
        return 'Filter: %s' % self.to_string()

    def match(self, data):
        raise NotImplementedError

    def to_string(self, indent=False, level=0, id_char=' '):
        id_str = self._indent(indent, level, id_char)
        id_str2 = id_str
        nl = '\n' if indent else ''

        if not Filter.collapsed and self.comp == '!':
            nl = ''
            id_str2 = ''
            indent = 0

        return ''.join([
            id_str,
            '(',
            self.comp,
            nl,
            nl.join(list(map(lambda x: x.to_string(indent, level + 1, id_char), self.filters))),
            nl,
            id_str2,
            ')'
        ])


class GroupOr(Group):
    def __init__(self, filters):
        super().__init__(comp='|', filters=filters)

    def match(self, data):
        return any(f.match(data) for f in self.filters)


class GroupAnd(Group):
    def __init__(self, filters):
        super().__init__(comp='&', filters=filters)

    def match(self, data):
        return any(f.match(data) for f in self.filters)


class GroupNot(Group):
    def __init__(self, filters):
        super().__init__(comp='!', filters=filters)

    def match(self, data):
        return not any(_not_helper(f, data) for f in self.filters)

    def simplify(self):
        return self


class Attribute:
    def __init__(self, name):
        self.name = name

    def present(self):
        return Filter(self.name, '=', '*')

    def raw(self, value):
        return Filter(self.name, '=', value)

    def equal_to(self, value):
        return Filter(self.name, '=', self.escape(value))

    def starts_with(self, value):
        return Filter(self.name, '=', self.escape(value) + '*')

    def ends_with(self, value):
        return Filter(self.name, '=', '*' + self.escape(value))

    def contains(self, value):
        return Filter(self.name, '=', '*' + self.escape(value) + '*')

    def approx(self, value):
        return Filter(self.name, '~=', self.escape(value))

    def lte(self, value):
        return Filter(self.name, '<=', self.escape(value))

    def gte(self, value):
        return Filter(self.name, '>=', self.escape(value))

    @staticmethod
    def escape(data):
        escaped = data.replace('\\', '\\5c')
        escaped = escaped.replace('*', '\\2a')
        escaped = escaped.replace('(', '\\28')
        escaped = escaped.replace(')', '\\29')
        escaped = escaped.replace('\x00', '\\00')

        return escaped


def _as_list(val):
    if not isinstance(val, (list, tuple)):
        return [val]

    return val


def _ss_regex(filt):
    pattern = re.sub(r'\*', '.*', filt)
    pattern = re.sub(r'(?<=\\)([0-9a-fA-F]{,2})', _ss_regex_escaped, pattern)
    return re.compile('^' + pattern + '$', re.I)


def _ss_regex_escaped(match):
    s = match.group(0) if match else None

    if s in ['28', '29', '5c', '2a']:
        s = '\\x{}'.format(match.group(0).upper())

    return s


def _ss_helper(cv, filt):
    regex = _ss_regex(filt)

    return regex.match(cv)


def _ms_helper(cv, filt):
    if cv:
        return cv.lower() == Filter.unescape(filt).lower()


def _lte_helper(cv, filt):
    return cv <= filt


def _gte_helper(cv, filt):
    return cv >= filt


def _not_helper(filt, data):
    try:
        return filt.match(data)
    except AttributeError:
        pass


def _g_to_string_helper(item, indent, level, id_char):
    return item.to_string(indent, level, id_char)

from datetime import datetime
import re


UNITS = {
    'trillions': 1000000000000,
    'billions': 1000000000,
    'millions': 1000000,
    'thousands': 1000,
    'hundreds': 100,
    'tens': 10,
    'ones': 1,
}


class Format(object):

    @staticmethod
    def as_is(s):
        return re.sub(r'[\n]', '', s)

    @staticmethod
    def as_str(s):
        s = s.lower().strip()
        s = re.sub(r'[,\n]', '', s)
        s = re.sub(r'[\s/]', '_', s)
        return s

    @staticmethod
    def as_int(s):
        s = re.sub(r'[^-\d]', '', s.strip())
        try:
            return int(s)
        except ValueError:
            return None

    @staticmethod
    def as_float(s):
        s = re.sub(r'[^-.%\d]', '', s.strip())
        divisor = 1
        if '%' in s:
            s = s.replace('%', '')
            divisor = 100
        try:
            return float(s) / divisor
        except ValueError:
            return None

    @staticmethod
    def as_currency(s):
        s = re.sub(r'[^-$.\d]', '', s.strip())
        return s if s else None

    @staticmethod
    def as_datetime(s):
        s = re.sub(r'[\n]', '', s.strip())
        try:
            return (datetime
                    .strptime(s, "%B %d, %Y")
                    .isoformat())
        except ValueError:
            return None

    @staticmethod
    def as_units(s):
        s = re.sub(r'[\n]', '', s.strip())
        if not s:
            return None, None, None
        matched = re.match(r'\(([A-Z][a-z]+)?\s?([A-Z]{1,4})?\s?(.)?\)', s)
        denom, country, currency = matched.groups()
        try:
            denom = denom.lower()
        except AttributeError:
            pass
        return UNITS.get(denom), country, currency

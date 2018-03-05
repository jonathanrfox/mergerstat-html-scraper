from datetime import datetime
import re


UNITS = {
    'ones':      10**0,
    'tens':      10**1,
    'hundreds':  10**2,
    'thousands': 10**3,
    'millions':  10**6,
    'billions':  10**9,
    'trillions': 10**12
}


def as_is(s):
    ''' returns string with no leading/trailing spaces '''
    return s.strip()


def as_str(s):
    ''' returns string with no commas, forward slashes and
    spaces converted to underscores, and letters all to lowercase '''
    s = s.lower().strip().replace(',', '')
    return re.sub(r'[\s/]', '_', s)


def as_int(s):
    ''' returns only dashes and numbers '''
    s = re.sub(r'[^-\d]', '', s.strip())
    try:
        return int(s)
    except ValueError:
        return None


def as_float(s):
    ''' converts percentages to decimal.
    returns only dashes, periods, and numbers '''
    s = re.sub(r'[^-.%\d]', '', s.strip())
    divisor = 1
    if '%' in s:
        s = s.replace('%', '')
        divisor = 100
    try:
        return float(s) / divisor
    except ValueError:
        return None


def as_currency(s):
    ''' returns only dashes, dollars, periods, and numbers '''
    return re.sub(r'[^-$.\d]', '', s.strip())


def as_datetime(s):
    try:
        return (datetime
                .strptime(s.strip(), "%B %d, %Y")
                .isoformat())
    except ValueError:
        return None


def as_units(s):
    s = s.strip()
    if not s:
        return None, None, None
    matched = re.match(r'\(([A-Z][a-z]+)?\s?([A-Z]{1,4})?\s?(.)?\)', s)
    denom, country, currency = matched.groups()
    try:
        denom = denom.lower()
    except AttributeError:
        pass
    return UNITS.get(denom), country, currency

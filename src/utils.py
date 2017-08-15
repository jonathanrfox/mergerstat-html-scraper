from datetime import datetime
import re
from typing import Optional, Union, Tuple


# consider different levels of cleaning
# -don't want to strip decimal points
# -don't want some long strings formatted
# -don't want datetime to be messed up

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
    def as_is(s: str) -> str:
        return re.sub(r'[\n]', '', s)

    @staticmethod
    def as_str(s: str) -> str:
        s = s.lower().strip()
        s = re.sub(r'[,\n]', '', s)
        s = re.sub(r'[\s/]', '_', s)
        return s

    @staticmethod
    def as_int(s: str) -> Union[int, str]:
        s = re.sub(r'[^-\d]', '', s.strip())
        try:
            return int(s)
        except ValueError:
            return None

    @staticmethod
    def as_float(s: str) -> Union[float, str]:
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
    def as_currency(s: str) -> str:
        s = re.sub(r'[^-$.\d]', '', s.strip())
        return s if s else None

    @staticmethod
    def as_datetime(s: str) -> str:
        s = re.sub(r'[\n]', '', s.strip())
        try:
            return (datetime
                    .strptime(s, "%B %d, %Y")
                    .isoformat())
        except ValueError:
            return None

    @staticmethod
    def as_units(s: str) -> Tuple[Optional[int], Optional[str], Optional[str]]:
        s = re.sub(r'[\n]', '', s.strip())
        if s == '':
            s = '(' + s + ')'
        matched = re.match(r'\(([A-Z][a-z]+)?\s?([A-Z]{1,4})?\s?(.)?\)', s)
        denom, country, currency = matched.groups()
        try:
            denom = denom.lower()
        except AttributeError:
            pass
        return UNITS.get(denom), country, currency

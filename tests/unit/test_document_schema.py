import re

from src.document_schema import DOCUMENT_SCHEMA
from src.utils import Format


FIND_METHODS = ['label', 'firstrow', 'header']

FORMAT_METHODS = [
    Format.as_is, Format.as_datetime,
    Format.as_int, Format.as_currency,
    Format.as_str, Format.as_float,
    Format.as_units
]

RECOMPILE_T = type(re.compile(r''))


def test_document_schema():
    for i, schema in enumerate(DOCUMENT_SCHEMA):
        assert schema.find_method in FIND_METHODS
        assert (schema.ref_pat is None or
                isinstance(schema.ref_pat, RECOMPILE_T))
        for record in schema.records:
            assert isinstance(record.key, str)
            assert isinstance(record.pat, RECOMPILE_T)
            assert record.fmt in FORMAT_METHODS

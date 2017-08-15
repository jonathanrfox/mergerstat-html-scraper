import pytest

from src.utils import Format


@pytest.mark.parametrize('input_str, expected', [
    ('A String\n', 'A String'),
    ('STRING\n', 'STRING'),
    ('1111\n', '1111')
])
def test_format_as_is(input_str, expected):
    actual = Format.as_is(input_str)
    assert actual == expected


@pytest.mark.parametrize('input_str, expected', [
    ('A String\n', 'a_string'),
    ('1111\n', '1111'),
    ('There, was\n', 'there_was'),
    ('This/That\n', 'this_that')
])
def test_format_as_str(input_str, expected):
    actual = Format.as_str(input_str)
    assert actual == expected


@pytest.mark.parametrize('input_str, expected', [
    ('1111\n', 1111),
    (' 230\n', 230),
    ('There, was', None),
    ('A String\n', None),
])
def test_format_as_int(input_str, expected):
    actual = Format.as_int(input_str)
    assert actual == expected


@pytest.mark.parametrize('input_str, expected', [
    ('123.01\n', 123.01),
    ('aaa88.3%aaa', 0.883),
    ('aaa123.01aaa\n', 123.01),
    ('A string\n', None)
])
def test_format_as_float(input_str, expected):
    actual = Format.as_float(input_str)
    assert actual == expected


@pytest.mark.parametrize('input_str, expected', [
    ('$123, 000, 000.01\n', '$123000000.01'),
    ('amount: $-123, 000.123\n', '$-123000.123'),
    ('$-0.203\n', '$-0.203'),
    ('$1.683\n', '$1.683'),
    ('a string\n', None)
])
def test_format_as_currency(input_str, expected):
    actual = Format.as_currency(input_str)
    assert actual == expected


@pytest.mark.parametrize('input_str, expected', [
    (' January 27, 2010\n ', '2010-01-27T00:00:00'),
    ('01-27-2010\n', None),
    ('27th of January 2010', None)
])
def test_format_as_datetime(input_str, expected):
    actual = Format.as_datetime(input_str)
    assert actual == expected


@pytest.mark.parametrize('input_str, expected', [
    (' (Trillions US $)\n ', (1000000000000, 'US', '$')),
    (' (Billions US $)\n ', (1000000000, 'US', '$')),
    (' (Millions US $)\n ', (1000000, 'US', '$')),
    (' (Thousands US $)\n ', (1000, 'US', '$')),
    (' (Hundreds US $)\n ', (100, 'US', '$')),
    (' (Tens US $)\n ', (10, 'US', '$')),
    (' (Ones US $)\n ', (1, 'US', '$')),
    (' (Ones US)\n ', (1, 'US', None)),
    (' (Ones $)\n ', (1, None, '$')),
    (' (Ones) ', (1, None, None)),
    (' (US $)\n ', (None, 'US', '$')),
    (' (US)\n ', (None, 'US', None)),
    (' ($)\n ', (None, None, '$')),
    ('', (None, None, None))

])
def test_format_as_units(input_str, expected):
    actual = Format.as_units(input_str)
    assert actual == expected

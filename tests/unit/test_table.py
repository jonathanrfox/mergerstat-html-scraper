import os
import re

import pytest

from src.table import Table
from tests.utils import mksoup


base_dir = os.path.dirname(__file__)

snippet_dir = os.path.join(base_dir, 'test_table_snippets')


@pytest.fixture(
    params=[
        ('table1_snippet.html', [
            (re.compile(r'^l1'), ('v1',))
        ]),
        ('table2_snippet.html', [
            (re.compile(r'^l1'), ('v1',)),
            (re.compile(r'^l2'), ('v2',))
        ]),
    ]
)
def table_maker(request):
    path = os.path.join(snippet_dir, request.param[0])
    soup = mksoup(path)
    table = Table(soup.find('table'))
    return table, request.param[1]


def test_table_init(table_maker):
    table, _ = table_maker
    assert table._rows is not None


def test_table_len(table_maker):
    table, expected = table_maker
    assert len(table) == len(expected)


def test_table_get(table_maker):
    table, _ = table_maker
    assert isinstance(table.rows, dict)
    assert table.rows is not None


def test_table_iterrows(table_maker):
    table, expected = table_maker
    for i, row in table.iterrows():
        assert expected[i][1] == row[1:]


def test_table_pop_row(table_maker):
    table, _ = table_maker
    keys = list(table.keys)
    while table.rows:
        table.pop_row(keys.pop())
    assert table.rows == {}


def test_table_find_match(table_maker):
    table, expected = table_maker
    for pat, val in expected:
        actual = table.find_match(pat)
        assert actual[1:] == val

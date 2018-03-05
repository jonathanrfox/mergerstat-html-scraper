import re

from bs4 import BeautifulSoup
import pytest

from mergerstat_scraper.table import Table


@pytest.fixture
def table():
    html = """
    <table>
    <tr><td>label</td><td>value</td></tr>
    </table>
    """
    return Table(BeautifulSoup(html, 'lxml').find('table'))


def test_Table_init(table):
    assert table._rows[0] == ('label', 'value')


def test_Table_len(table):
    assert len(table._rows) == 1


def test_Table_getitem(table):
    assert table[0] == ('label', 'value')


def test_Table_iterrows(table):
    for key, row in table.iterrows():
        assert row == table._rows[key]


def test_Table_pop_row(table):
    row_count = len(table)
    table.pop_row(0)
    assert len(table) == row_count - 1


def test_Table_find_match(table):
    val = table.find_match(re.compile(r'^label.*'), out_col=1)
    assert val == 'value'


def test_Table_find_match_returns_tuple(table):
    val = table.find_match(re.compile(r'^label.*'))
    assert val == ('label', 'value')

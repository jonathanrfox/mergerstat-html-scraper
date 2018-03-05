import re

from bs4 import BeautifulSoup

from mergerstat_scraper.tag_finder import *


def test_sanity():
    assert True == True


def test_find_tag_by_label():
    expected = 'value'
    html = f"""
    <a name="DOC_ID_0"></a>
    <span>label</span>
    <span>{expected}</b></span>
    """
    soup = BeautifulSoup(html, 'lxml')
    root = soup.find_all('a')[0]
    actual = find_tag_by_label(root, re.compile(r'.*label.*'))
    assert actual.text == expected


def test_find_table_by_first_row():
    expected = 'tbl'
    html = f"""
    <a name="DOC_ID_0"></a>
    <table id="{expected}">
    <tr><td>label<td></tr>
    </table>
    """
    soup = BeautifulSoup(html, 'lxml')
    root = soup.find_all('a')[0]
    actual = find_table_by_first_row(root, re.compile(r'.*label.*'))
    assert actual.get('id') == expected


def test_find_table_by_header():
    expected = 'tbl'
    html = f"""
    <a name="DOC_ID_0"></a>
    <h1>label</h1>
    <table id="{expected}">
    </table>
    """
    soup = BeautifulSoup(html, 'lxml')
    root = soup.find_all('a')[0]
    actual = find_table_by_header(root, re.compile(r'.*label.*'))
    assert actual.get('id') == expected


def test_root_tags_match_returns_true():
    html = f"""
    <a name="DOC_ID_0"></a>
    <table id="tbl"></table>
    """
    soup = BeautifulSoup(html, 'lxml')
    root = soup.find_all('a')[0]
    table = root.find_next('table')
    actual = root_tags_match(root, table)
    assert actual == True


def test_root_tags_match_returns_false():
    html = f"""
    <a name="DOC_ID_0"></a>
    <a name="DOC_ID_1"></a>
    <table id="tbl"></table>
    """
    soup = BeautifulSoup(html, 'lxml')
    root = soup.find_all('a')[0]
    table = root.find_next('table')
    actual = root_tags_match(root, table)
    assert actual == False

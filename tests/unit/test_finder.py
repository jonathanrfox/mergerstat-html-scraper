from unittest.mock import Mock, patch, call

import pytest

from src.finder import Finder


@pytest.fixture
def mock_tag():
    _mock_tag = Mock()
    fn1 = _mock_tag.find_next.return_value
    fn1.find_next.return_value = 'rv'
    fn1.find_previous.return_value = 'rv'
    return _mock_tag


def test_finder_init():
    finder = Finder(None)
    assert finder.root_tag is None


def test_finder_find_tag_by_label(mock_tag):
    finder = Finder(mock_tag)
    assert finder.find_tag_by_label('label') == 'rv'


def test_finder_find_table_by_first_row(mock_tag):
    finder = Finder(mock_tag)
    assert finder.find_table_by_first_row('label') == 'rv'


def test_finder_find_table_by_header(mock_tag):
    finder = Finder(mock_tag)
    assert finder.find_table_by_header('label') == 'rv'


def test_finder_find():
    mock_findfn = Mock(return_value='rv')
    call_with = 'args'
    with patch.object(Finder, '_verify_tag') as mock_verify_tag:
        finder = Finder(None)
        finder.find(mock_findfn, call_with)
        assert mock_verify_tag.call_count == 1
    assert mock_findfn.call_args == call(call_with)


@pytest.mark.parametrize('root_name, other_name, expected', [
    ('A', 'A', True),
    ('A', 'B', False)
])
def test_finder_root_tag_names_match(root_name, other_name, expected):
    root_tag = {'name': root_name}
    mock_other_tag = Mock()
    mock_other_tag.find_previous.return_value = {'name': other_name}
    finder = Finder(root_tag)
    actual = finder._root_tag_names_match(mock_other_tag)
    assert actual == expected
    assert mock_other_tag.find_previous.call_count == 1

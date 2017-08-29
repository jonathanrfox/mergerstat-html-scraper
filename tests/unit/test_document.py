from unittest.mock import call, Mock, patch

import pytest

from src.document import Document
from src.finder import Finder
from src.templates import RecordTemplate, SchemaTemplate
from src.table import Table


@pytest.fixture(params=[
    ('key1', 'pat1', 'fmt1'),
    ('units', 'pat2', 'fmt2')
])
def mock_record(request):
    _mock_record = (
        RecordTemplate(
            key=request.param[0],
            pat=request.param[1],
            fmt=Mock(return_value=request.param[2])
        ),
    )
    return _mock_record


@pytest.fixture(params=[
    'label', 'firstrow', 'header'
])
def mock_schema(request, mock_record):
    _mock_schema = (
        SchemaTemplate(
            records=mock_record,
            ref_pat='pat',
            find_method=request.param
        ),
    )
    return _mock_schema


@pytest.fixture
def mock_finder():
    _mock_finder = Mock(Finder)
    _mock_finder.root_tag = {'name': None}
    _mock_finder.find.return_value = None
    _mock_finder.find_tag_by_label.return_value = None
    _mock_finder.find_table_by_first_row.return_value = None
    _mock_finder.find_table_by_header.return_value = None
    return _mock_finder


@pytest.fixture(params=['match1', 'match2', 'match3', None])
def mock_table(request):
    _mock_table = Mock(Table)
    _mock_table.find_match.return_value = request.param
    return _mock_table


def test_document_init():
    document = Document(Mock(), Mock())
    assert document.result == {}


# @pytest.mark.skip(reason="refactoring")
def test_document_build(mock_schema, mock_finder):
    if mock_schema[0].find_method == 'label':
        build_fn = '_build_from_label'
    else:
        build_fn = '_build_from_table_tag'

    with patch.object(Document, build_fn) as mock_func:
        document = Document(mock_schema, mock_finder)
        document.build()
        assert mock_func.call_count == 1


@pytest.mark.parametrize('mff_rv', [
    Mock(text='text'), None
])
def test_document_build_from_label(mff_rv, mock_schema, mock_finder):
    mock_find_by_fn = Mock()
    mock_record = mock_schema[0].records[0]
    mock_finder.find.return_value = mff_rv

    document = Document(Mock(), mock_finder)
    document._build_from_label(mock_find_by_fn, mock_schema[0])

    assert mock_finder.find.call_count == 1
    assert mock_finder.find.call_args == call(mock_find_by_fn, mock_record.pat)

    exp_result = mock_record.fmt() if mff_rv else None
    assert document._result[mock_record.key] == exp_result


@patch('src.document.Table')
@pytest.mark.parametrize('table_tag, doc_func', [
    (None, '_fill_none'),
    ('a table tag', '_build_from_table')
])
def test_document_build_from_table_tag(table, table_tag, doc_func, mock_schema,
                                       mock_finder):
    mock_find_by_fn = Mock()
    records = mock_schema[0].records
    ref_pat = mock_schema[0].ref_pat
    mock_finder.find.return_value = table_tag

    with patch.object(Document, doc_func) as mock_doc_func:
        document = Document(Mock(), mock_finder)
        document._build_from_table_tag(mock_find_by_fn, mock_schema[0])

        #checking find
        assert mock_finder.find.call_count == 1
        assert mock_finder.find.call_args == call(mock_find_by_fn, ref_pat)

        # checking doc_func
        assert mock_doc_func.call_count == 1

        exp_mdf_call_args = call(records, table()) if table_tag else call(records)
        assert mock_doc_func.call_args == exp_mdf_call_args


def test_document_fill_none(mock_finder, mock_record):
    document = Document(Mock(), mock_finder)
    document._fill_none(mock_record)
    for record in mock_record:
        assert document._result[record.key] is None


def test_document_build_from_table(mock_finder, mock_record, mock_table):
    document = Document(Mock(), mock_finder)
    document._build_from_table(mock_record, mock_table)
    assert mock_table.find_match.call_count == 1
    for record in mock_record:
        assert record.fmt.call_count in [0, 1]
        assert document._result[record.key] in [record.fmt(), None]

from typing import Any, Callable, Dict, Optional, Pattern, Tuple, Union

from .finder import Finder
from .table import Table
from .templates import RecordTemplate, SchemaTemplate


Tag = Any


class Document(object):

    def __init__(self, doc_schema: Tuple[SchemaTemplate, ...],
                 finder: Finder) -> None:

        self.doc_schema = doc_schema
        self.finder = finder

        self.dispatcher: Dict[str, Tuple[Any, Any]]
        self.dispatcher = {
            'label': (self._build_from_label,
                      self.finder.find_tag_by_label),
            'firstrow': (self._build_from_table_tag,
                         self.finder.find_table_by_first_row),
            'header': (self._build_from_table_tag,
                       self.finder.find_table_by_header)
        }

        self._result: Dict[str, Optional[Union[int, float, str]]]
        self._result = {}

    def _get_build_and_find_fns(self, key):

        return self.dispatcher.get(key, (None, None))

    def build(self) -> None:

        for schema in self.doc_schema:
            build_fn, find_by_fn = self._get_build_and_find_fns(
                schema.find_method)

            if build_fn and find_by_fn:
                build_fn(find_by_fn, schema)

    @property
    def result(self) -> Dict[str, Optional[Union[int, float, str]]]:
        return self._result

    def _build_from_label(
            self,
            find_by_fn: Callable[[Pattern[str]], Optional[Tag]],
            schema: SchemaTemplate) -> None:

        for key, pat, fmt in schema.records:
            # val = self.finder.find_tag_by_label(pat)
            val = self.finder.find(find_by_fn, pat)
            self._result[key] = fmt(val.text) if val else None

    def _build_from_table_tag(
            self,
            find_by_fn: Callable[[Pattern[str]], Optional[Tag]],
            schema: SchemaTemplate) -> None:

        table_tag = self.finder.find(find_by_fn, schema.ref_pat)
        if not table_tag:
            self._fill_none(schema.records)
        else:
            table = Table(table_tag)
            self._build_from_table(schema.records, table)

    def _fill_none(self, records: Tuple[RecordTemplate, ...]) -> None:

        for record in records:
            self._result[record.key] = None

    def _build_from_table(self, records: Tuple[RecordTemplate, ...],
                          table: Table) -> None:

        for key, pat, fmt in records:
            if 'units' in key:
                out_col = 0
            else:
                out_col = 1
            val = table.find_match(pat, in_col=0, out_col=out_col)
            self._result[key] = (fmt(val)
                                 if val and isinstance(val, str)
                                 else None)

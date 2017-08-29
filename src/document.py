from .finder import Finder
from .table import Table
from .templates import RecordTemplate, SchemaTemplate


class Document(object):

    def __init__(self, doc_schema, finder):
        self.doc_schema = doc_schema
        self.finder = finder
        self._result = {}

    def build(self):
        for schema in self.doc_schema:
            if schema.find_method == 'label':
                self._build_from_label(self.finder.find_tag_by_label,
                                       schema)

            elif schema.find_method == 'firstrow':
                self._build_from_table_tag(self.finder.find_table_by_first_row,
                                           schema)

            elif schema.find_method == 'header':
                self._build_from_table_tag(self.finder.find_table_by_header,
                                           schema)

    @property
    def result(self):
        return self._result

    def _build_from_label(self, find_by_fn, schema):
        for key, pat, fmt in schema.records:
            val = self.finder.find(find_by_fn, pat)
            self._result[key] = fmt(val.text) if val else None

    def _build_from_table_tag(self, find_by_fn, schema):
        table_tag = self.finder.find(find_by_fn, schema.ref_pat)
        if not table_tag:
            self._fill_none(schema.records)
        else:
            table = Table(table_tag)
            self._build_from_table(schema.records, table)

    def _fill_none(self, records):
        for record in records:
            self._result[record.key] = None

    def _build_from_table(self, records, table):
        for key, pat, fmt in records:
            out_col = 0 if 'units' in key else 1
            val = table.find_match(pat, in_col=0, out_col=out_col)
            self._result[key] = fmt(val) if val else None



class Table(object):

    def __init__(self, table):
        self._rows = {}
        for i, row in enumerate(table.find_all('tr')):
            self._rows[i] = tuple([cell.text for cell in row.find_all('td')])

    def __len__(self):
        return len(self._rows)

    def __getitem__(self, key):
        return self._rows.get(key)

    @property
    def keys(self):
        return list(self._rows.keys())

    @property
    def rows(self):
        return self._rows

    def iterrows(self):
        for key, row in self._rows.items():
            yield key, row

    def pop_row(self, key):
        return self._rows.pop(key)

    def find_match(self, pat, in_col=0, out_col=None):
        for key, row in self._rows.items():
            if pat.match(row[in_col]):
                if out_col is not None:
                    return self.pop_row(key)[out_col]
                else:
                    return self.pop_row(key)

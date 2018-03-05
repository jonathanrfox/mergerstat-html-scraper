class Table(object):

    def __init__(self, raw_table):
        self._rows = {}
        for i, row in enumerate(raw_table.find_all('tr')):
            self._rows[i] = tuple(cell.text for cell in row.find_all('td'))

    def __len__(self):
        return len(self._rows)

    def __getitem__(self, key):
        return self._rows.get(key)

    def iterrows(self):
        for key, row in self._rows.items():
            yield key, row

    def pop_row(self, key):
        return self._rows.pop(key)

    def find_match(self, pat, in_col=0, out_col=None):
        """
        :param pat: the pattern used for matching.
        :param in_col: used to specify the col for pat to match.
        :param out_col: used to specify the col to return, defaults to all.
        """
        for key, row in self.iterrows():
            if pat.match(row[in_col]):
                found = self.pop_row(key)
                if out_col is not None:
                    return found[out_col]
                return found

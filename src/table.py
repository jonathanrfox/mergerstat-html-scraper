from typing import Any, Dict, Iterator, List, Optional, Pattern, Tuple, Union


Tag = Any


class Table(object):

    def __init__(self, table: Tag) -> None:
        self._rows: Dict[int, Tuple[str, ...]]
        self._rows = {}
        for i, row in enumerate(table.find_all('tr')):
            self._rows[i] = tuple([cell.text for cell in row.find_all('td')])

    def __len__(self) -> int:
        return len(self._rows)

    def __getitem__(self, key: int) -> Tuple[str, ...]:
        return self._rows.get(key)

    @property
    def keys(self) -> List[int]:
        return list(self._rows.keys())

    @property
    def rows(self) -> Dict[int, Tuple[str, ...]]:
        return self._rows

    def iterrows(self) -> Iterator[Tuple[int, Tuple[str, ...]]]:
        for key, row in self._rows.items():
            yield key, row

    def pop_row(self, key: int) -> Tuple[str, ...]:
        return self._rows.pop(key)

    def find_match(self, pat: Pattern[str], in_col: int=0,
                   out_col: int=None) -> Optional[Union[str, Tuple[str, ...]]]:
        for key, row in self._rows.items():
            if pat.match(row[in_col]):
                if out_col is not None:
                    return self.pop_row(key)[out_col]
                return self.pop_row(key)
        return None

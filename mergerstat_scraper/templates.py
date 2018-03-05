from typing import Any, Callable, NamedTuple, Pattern


class RecordTemplate(NamedTuple):
    key: str                  # string to be used in result dict for value found
    pat: Pattern[str]         # pattern used to find label which finds value
    fmt: Callable[[str], Any] # format function used to clean value found


class RowRecordTemplate(NamedTuple):
    key: str                  # string to be used in result dict for value found
    pat: Pattern[str]         # pattern used to find label which finds value
    fmt: Callable[[str], Any] # format function used to clean value found
    in_col: int = 0           # column to match
    out_col: int = 1          # column to return

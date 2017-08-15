from typing import Any, Callable, NamedTuple, Optional, Pattern, Tuple, Union


# key: string to be used in result dict for value found
# pat: pattern used to find label which finds value
# fmt: format function used to clean value found

class RecordTemplate(NamedTuple):
    key: str
    pat: Pattern[str]
    fmt: Callable[[str], Any]


# find_method: string indicating which find method to use
# ref_pat: pattern used to find starting point for labels
# labels: a tuple of LabelTemplates

class SchemaTemplate(NamedTuple):
    find_method: str
    ref_pat: Optional[Pattern[str]]
    records: Tuple[RecordTemplate, ...]

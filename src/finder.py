import re
from typing import Any, Callable, Optional, Pattern

# notes
# - a lot of repetition in find methods, maybe combine into
#   one method

Tag = Any


class Finder(object):
    
    ROOT_TAG_NAME = 'a'
    ROOT_TAG_ATTRS = {'name': re.compile(r'^DOC_ID.*')}

    def __init__(self, root_tag: Tag) -> None:
        
        self.root_tag = root_tag

    def find_tag_by_label(self, label: Pattern[str]) -> Optional[Tag]:
        
        return (self.root_tag
                .find_next(text=label)
                .find_next('span'))

    def find_table_by_first_row(self, first_row: Pattern[str]) -> Optional[Tag]:
        
        return (self.root_tag
                .find_next(text=first_row)
                .find_previous('table'))

    def find_table_by_header(self, header: Pattern[str]) -> Optional[Tag]:
        
        return (self.root_tag
                .find_next(text=header)
                .find_next('table'))

    def find(self, findfn: Callable[[Pattern[str]], Optional[Tag]],
             pattern: Pattern[str]) -> Optional[Tag]:
        found_tag = None
        try:
            found_tag = findfn(pattern)
        except AttributeError:
            pass
        return self._verify_tag(found_tag)

    def _verify_tag(self, tag: Tag) -> Optional[Tag]:
        
        if not tag or not self._root_tag_names_match(tag):
            return None
        return tag.extract()

    def _root_tag_names_match(self, tag: Tag) -> bool:
        
        prev_root_tag = tag.find_previous(
            self.ROOT_TAG_NAME, self.ROOT_TAG_ATTRS)
        return self.root_tag['name'] == prev_root_tag['name']

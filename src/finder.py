import re


class Finder(object):

    ROOT_TAG_NAME = 'a'
    ROOT_TAG_ATTRS = {'name': re.compile(r'^DOC_ID.*')}

    def __init__(self, root_tag):
        self.root_tag = root_tag

    def find_tag_by_label(self, label_pat):
        return (self.root_tag
                .find_next(text=label_pat)
                .find_next('span'))

    def find_table_by_first_row(self, first_row_pat):
        return (self.root_tag
                .find_next(text=first_row_pat)
                .find_previous('table'))

    def find_table_by_header(self, header_pat):
        return (self.root_tag
                .find_next(text=header_pat)
                .find_next('table'))

    def find(self, findfn, pattern):
        found_tag = None
        try:
            found_tag = findfn(pattern)
        except AttributeError:
            pass
        return self._verify_tag(found_tag)

    def _verify_tag(self, tag):
        if not tag or not self._root_tag_names_match(tag):
            return None
        return tag.extract()

    def _root_tag_names_match(self, tag):
        prev_root_tag = tag.find_previous(self.ROOT_TAG_NAME,
                                          self.ROOT_TAG_ATTRS)
        return self.root_tag['name'] == prev_root_tag['name']

import re


ROOT_TAG_NAME = 'a'
ROOT_TAG_ATTRS = {'name': re.compile(r'^DOC_ID.*')}


def find_tag_by_label(root_tag, label_pat, tag_name='span'):
    try:
        tag = (root_tag
               .find_next(text=label_pat)
               .find_next(tag_name))
        if root_tags_match(root_tag, tag):
            print('tags match')
            return tag.extract()
    except AttributeError:
        pass
    print('tags don\'t match')


def find_table_by_first_row(root_tag, first_row_pat):
    try:
        tag = (root_tag
               .find_next(text=first_row_pat)
               .find_previous('table'))
        if root_tags_match(root_tag, tag):
            return tag.extract()
    except AttributeError:
        pass


def find_table_by_header(root_tag, header_pat):
    try:
        tag = (root_tag
               .find_next(text=header_pat)
               .find_next('table'))
        if root_tags_match(root_tag, tag):
            return tag.extract()
    except AttributeError:
        pass


def root_tags_match(root_tag, tag):
    try:
        other_root_tag = tag.find_previous(ROOT_TAG_NAME, ROOT_TAG_ATTRS)
        return root_tag['name'] == other_root_tag['name']
    except (AttributeError, KeyError):
        pass

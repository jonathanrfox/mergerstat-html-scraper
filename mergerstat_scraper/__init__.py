import os

from bs4 import BeautifulSoup

from .tag_finder import ROOT_TAG_NAME, ROOT_TAG_ATTRS


def scrape(filename, **components):
    '''
    Params:
        - filename: a path to a mergerstat html document.
        - components: a dict mapping strings to classes that implement
          DocumentComponent.
    Returns:
        - a generator yielding the components dict after calling extract on the
          class, as well as, the document id, and source file..
    '''
    with open(filename) as f:
        soup = BeautifulSoup(f, 'lxml')
    assert(soup)

    basename = os.path.basename(filename)

    for root_tag in soup.find_all(ROOT_TAG_NAME, ROOT_TAG_ATTRS):
        dct = {k: C.extract(root_tag) for k, C in components.items()}
        dct['document_id'] = root_tag['name']
        dct['source_file'] = basename
        yield dct

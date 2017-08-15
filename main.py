import os
from pprint import pprint
import re
import sys

from bs4 import BeautifulSoup
from pymongo import MongoClient

from src.document import Document
from src.document_schema import DOCUMENT_SCHEMA
from src.finder import Finder


client = MongoClient('mongodb://localhost')
db = client.merger_db


def main():
    soup = None
    with open(sys.argv[1]) as f:
        soup = BeautifulSoup(f, 'lxml')

    if not soup:
        raise ValueError('soup was None')

    attrs = {'name': re.compile(r'^DOC_ID.*')}

    for root_tag in soup.find_all('a', attrs):
        finder = Finder(root_tag)
        document = Document(DOCUMENT_SCHEMA, finder)
        document.build()

        doc = document.result
        doc['src_file'] = sys.argv[1]
        doc['doc_id'] = root_tag['name']

        db.merger_collection.update_one(
            {'deal_no': doc['deal_no']},
            {'$set': doc},
            upsert=True)


if __name__ == '__main__':
    main()

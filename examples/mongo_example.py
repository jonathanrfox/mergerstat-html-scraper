import pymongo
from pymongo import MongoClient

from ..mergerstat_scraper import scrape


def ensure_index(collection):
    if 'document_id_1' not in collection.index_information():
        collection.create_index(
            [('document_id', pymongo.ASCENDING)],
            unique=True
        )


def insert_document(collection, document):
    try:
        collection.insert_one(document)
    except pymongo.errors.DuplicateKeyError as e:
        pass


def main():
    filename = './example.html'

    client = MongoClient('mongodb://localhost')
    assert(client)

    collection = client.merger_db.merger_collection
    ensure_index(collection)

    for document in scrape(filename):
        insert_document(collection, document)


if __name__ == '__main__':
    main()

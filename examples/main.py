import os
from pprint import pprint
import sys

sys.path.append(os.path.abspath('.'))

from mergerstat_scraper import scrape


def main():
    filename = sys.argv[1]

    for document in scrape(filename):
        pprint(document)


if __name__ == '__main__':
    main()

from pprint import pprint
import sys

from mergerstat_scraper import scrape


def main():
    filename = './inputs/ExampleMerger.html'
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    for document in scrape(filename):
        pprint(document)


if __name__ == '__main__':
    main()

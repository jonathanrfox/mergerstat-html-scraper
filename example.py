from pprint import pprint
import sys

from mergerstat_scraper import scrape
from mergerstat_scraper.document_components import *


def main():
    filename = './inputs/ExampleMerger.html'
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    components = dict(
        metadata=DocumentMetadata,
        trans_summary=TransactionSummary,
        buyer_details=BuyerDetails,
        seller_details=SellerDetails,
        target_details=TargetDetails
    )

    for document in scrape(filename, **components):
        pprint(document)


if __name__ == '__main__':
    main()

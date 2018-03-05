from bs4 import BeautifulSoup

from .document_components import *
from .tag_finder import ROOT_TAG_NAME, ROOT_TAG_ATTRS


def scrape(filename):
    with open(filename) as f:
        soup = BeautifulSoup(f, 'lxml')
    assert(soup)

    for root_tag in soup.find_all(ROOT_TAG_NAME, ROOT_TAG_ATTRS):
        yield {
            **DocumentMetaData.extract(root_tag),
            'source_file': filename,
            'document_id': root_tag['name'],
            'transaction_summary': TransactionSummary.extract(root_tag),
            'buyer_details': BuyerDetails.extract(root_tag),
            'seller_details': SellerDetails.extract(root_tag),
            'target_details': TargetDetails.extract(root_tag),
            'financial_summary': FinancialSummary.extract(root_tag),
            'latest_twelve_months': LatestTwelveMonths.extract(root_tag)
        }

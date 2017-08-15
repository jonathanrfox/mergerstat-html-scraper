import os
import re

from bs4 import BeautifulSoup

from src.document import Document
from src.document_schema import DOCUMENT_SCHEMA
from src.finder import Finder


def test_google_doubleclick():
    expected = {
        'announce_date': '2007-04-13T00:00:00',
        'attitude': None,
        'base_equity': '$3100000000',
        'book_value': None,
        'buyer': 'Google, Inc.',
        'buyer_exchange': 'NASDAQ',
        'buyer_legal_status': 'public',
        'buyer_primary_industry': 'Computer Software, Supplies & Services',
        'buyer_ticker': 'GOOG',
        'cancelled_date': None,
        'cash_and_marketable_securities': None,
        'cash_payment': '$3100000000',
        'closing_date': '2008-03-11T00:00:00',
        'current_long_term_debt': None,
        'deal_description': 'Google Inc acquired DoubleClick Inc from Hellman & '
        'Friedman LLC, JMI Inc, and management for US$3.1 billion '
        'in cash. The acquisition allows Google Inc to offer '
        'superior tools for targeting, serving, and analyzing '
        'online ads of all types, significantly benefiting '
        'customers and consumers. In addition, the acquisition '
        "strengthens Google Inc's advertising network with "
        'expanded access to publisher inventory. DoubleClick Inc '
        'is a New York-based provider of marketing technology and '
        'services with 17 offices and 15 data centers worldwide.',
        'deal_no': 418068,
        'deal_type': 'divestiture',
        'doc_id': 'DOC_ID_0_118',
        'liabilities_assumed': None,
        'long_term_debt': None,
        'ltm_net_income': None,
        'ltm_revenue': '300.000',
        'ltm_units': (1000000, 'US', '$'),
        'method_of_payment': 'cash',
        'multiple_of_book_value': None,
        'original_offer_price': '$3100000000',
        'percent_sought': 1.0,
        'premium_offered': None,
        'price_earnings': None,
        'purpose': 'horizontal',
        'seller_breakup_fee': None,
        'share_price': None,
        'share_price_1_day_prior': '$467.390',
        'share_price_30_days_prior': '$448.230',
        'share_price_5_days_prior': '$471.510',
        'stock_exchange_ratio': None,
        'stock_payment': None,
        'target': 'DoubleClick, Inc.',
        'target_country': 'United States',
        'target_exchange': 'NASDAQ',
        'target_industry': 'Internet; Miscellaneous Services',
        'target_ticker': None,
        'total_assets': None,
        'total_invested_capital': '$3100000000',
        'total_invested_capital_over_ebitda': None,
        'transaction_notes': None,
        'transaction_type': 'Divestiture'
    }


    root = os.path.dirname(__file__)
    path = os.path.join(root, 'google_doubleclick.html')

    with open(path) as f:
        soup = BeautifulSoup(f, 'lxml')

    attrs = {'name': re.compile(r'^DOC_ID.*')}
    root_tag = soup.find_all('a', attrs)[0]

    finder = Finder(root_tag)
    document = Document(DOCUMENT_SCHEMA, finder)
    document.build()
    actual = document.result
    actual['doc_id'] = root_tag['name']

    assert actual == expected

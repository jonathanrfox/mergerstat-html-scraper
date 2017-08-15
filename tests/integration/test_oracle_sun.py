import os
import re

from bs4 import BeautifulSoup

from src.document import Document
from src.document_schema import DOCUMENT_SCHEMA
from src.finder import Finder


def test_oracle_sun():
    expected = {
        'announce_date': '2009-04-20T00:00:00',
        'attitude': None,
        'base_equity': '$7074701158',
        'book_value': '$1254000000',
        'buyer': 'Oracle Corp.',
        'buyer_exchange': 'NASDAQ',
        'buyer_legal_status': 'public',
        'buyer_primary_industry': 'Computer Software, Supplies & Services',
        'buyer_ticker': 'ORCL',
        'cancelled_date': None,
        'cash_and_marketable_securities': '$1569000000',
        'cash_payment': '$7074701158',
        'closing_date': '2010-01-27T00:00:00',
        'current_long_term_debt': '$562000000',
        'deal_description': 'Oracle Corp acquired Sun Microsystems Inc for '
        'approximately $7.1 billion in cash, or $9.50 per share. '
        'The transaction follows the failed attempts from IBM and '
        'Sun to complete their previously announced transaction. '
        'Oracle cited the Solaris technologies of Sun '
        'Microsystems Inc as a key attraction for doing the deal. '
        'In addition, Oracle Corp owns the MySQL database, which '
        'Sun had acquired in 2008.',
        'deal_no': 510696,
        'deal_type': 'acquisition',
        'doc_id': 'DOC_ID_0_46',
        'liabilities_assumed': None,
        'long_term_debt': '$695000000',
        'ltm_net_income': '-151.000',
        'ltm_revenue': '12604.000',
        'ltm_units': (1000000, 'US', '$'),
        'method_of_payment': 'cash',
        'multiple_of_book_value': 5.642,
        'original_offer_price': '$7074701000',
        'percent_sought': 1.0,
        'premium_offered': 0.48,
        'price_earnings': -46.852,
        'purpose': 'horizontal',
        'seller_breakup_fee': '$260000000',
        'share_price': '$9.500000',
        'share_price_1_day_prior': '$6.690',
        'share_price_30_days_prior': '$3.950',
        'share_price_5_days_prior': '$6.420',
        'stock_exchange_ratio': None,
        'stock_payment': None,
        'target': 'Sun Microsystems, Inc.',
        'target_country': 'United States',
        'target_exchange': 'NASDAQ',
        'target_industry': 'Internet; Electronics',
        'target_ticker': 'JAVA',
        'total_assets': '$11262000000',
        'total_invested_capital': '$8331701000',
        'total_invested_capital_over_ebitda': 11.079,
        'transaction_notes': 'BE=744,705,385 JAVA o/s * $9.50 cash offer',
        'transaction_type': 'Acquisition of Public Company'
    }

    root = os.path.dirname(__file__)
    path = os.path.join(root, 'oracle_sun.html')

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

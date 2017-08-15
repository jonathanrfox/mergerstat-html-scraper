import os
import re

from bs4 import BeautifulSoup

from src.document import Document
from src.document_schema import DOCUMENT_SCHEMA
from src.finder import Finder


def test_facebook_whatsapp():
    expected = {
        'announce_date': '2014-02-19T00:00:00',
        'attitude': None,
        'base_equity': '$19645174481',
        'book_value': None,
        'buyer': 'Facebook, Inc.',
        'buyer_exchange': 'NASDAQ',
        'buyer_legal_status': 'public',
        'buyer_primary_industry': 'Miscellaneous Services',
        'buyer_ticker': 'FB',
        'cancelled_date': None,
        'cash_and_marketable_securities': None,
        'cash_payment': '$4590000000',
        'closing_date': '2014-10-06T00:00:00',
        'current_long_term_debt': None,
        'deal_description': 'Facebook Inc acquired WhatsApp Inc from Sequoia Capital, '
        'Mr. Jan Koum and Mr. Brian Acton, for US$21.9 billion in '
        'cash and stock. Under the terms of the agreement, '
        'Facebook Inc paid US$4.6 billion in cash and issued '
        '177.8 million class A common shares to WhatsApp Inc. In '
        'addition, the Facebook Inc would also grant 45.9 million '
        "restricted stock units to WhatsApp Inc's employees. The "
        "cash consideration was funded through Facebook Inc's "
        'existing cash balance of US$11.5 billion as of December '
        '31, 2013. The acquisition would help accelerate Facebook '
        "Inc's growth, strengthening its connectivity and utility "
        'worldwide. The transaction was subject to regulatory '
        "approvals. Upon closing, Mr. Koum, WhatsApp Inc's "
        'co-founder and CEO, would become a member of Facebook '
        "Inc's board of directors. The acquisition was expected "
        'to close later in 2014. The agreement could have been '
        'terminated by either party if the closing has not '
        'occurred on or before August 19, 2014 or if all '
        'conditions have been completed by August 19, 2014 except '
        'for the approval of the regulatory bodies. WhatsApp Inc '
        'is located in Santa Clara, California, United States and '
        'develops a cross platform mobile messenger that replaces '
        'SMS. On March 7, 2014, privacy groups Electronic Privacy '
        'Information Center and Center For Digital Democracy '
        'asked US the Federal Trade Commission, to suspend the '
        'transaction in order for it to investigate where '
        "Facebook Inc would be using WhatsApp Inc's subscriber "
        'data. On April 9, 2014, the Federal Trade Commission '
        'cleared the transaction. On May 28, 2014, Facebook Inc '
        'sought the approval from the European antitrust '
        'regulators regarding the transaction. On July 9, 2014, '
        'the European Union (EU) antitrust officials began '
        'questioning rival firms about the deal before they start '
        'a formal merger review that could be a test case for how '
        'to apply EU competition law to social media. On '
        'September 1, 2014, the European Commission (EC) '
        'announced that it would decide the approval of the '
        'transaction by October 3, 2014. As of September 25, '
        '2014, sources said that the EC is likely to approve the '
        'transaction. On October 4, 2014, the EC approved the '
        'transaction.',
        'deal_no': 779945,
        'deal_type': 'acquisition',
        'doc_id': 'DOC_ID_0_1',
        'liabilities_assumed': None,
        'long_term_debt': None,
        'ltm_net_income': None,
        'ltm_revenue': None,
        'ltm_units': None,
        'method_of_payment': 'combo',
        'multiple_of_book_value': None,
        'original_offer_price': None,
        'percent_sought': 1.0,
        'premium_offered': None,
        'price_earnings': None,
        'purpose': 'horizontal',
        'seller_breakup_fee': None,
        'share_price': None,
        'share_price_1_day_prior': '$67.300',
        'share_price_30_days_prior': '$57.200',
        'share_price_5_days_prior': '$64.851',
        'stock_exchange_ratio': None,
        'stock_payment': '$15055174481',
        'target': 'WhatsApp, Inc.',
        'target_country': 'United States',
        'target_exchange': None,
        'target_industry': 'Computer Software, Supplies & Services',
        'target_ticker': None,
        'total_assets': None,
        'total_invested_capital': '$19645174000',
        'total_invested_capital_over_ebitda': None,
        'transaction_notes': None,
        'transaction_type': 'Acquisition of Private Company'
    }

    root = os.path.dirname(__file__)
    path = os.path.join(root, 'facebook_whatsapp.html')

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

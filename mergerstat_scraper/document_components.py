from abc import ABC, abstractmethod
import re

from .table import Table
from .tag_finder import *
from .templates import RecordTemplate, RowRecordTemplate
from .utils import *


def fill_none(records):
    return {key: None for key, *_ in records}


def extract_table(raw_table, records):
    if not raw_table:
        return fill_none(records)
    result = {}
    table = Table(raw_table)
    for key, pat, fmt, in_col, out_col in records:
        value = table.find_match(pat, in_col=in_col, out_col=out_col)
        if value is not None:
            result[key] = fmt(value)
        else:
            result[key] = None
    return result


class DocumentComponent(ABC):
    @classmethod
    @abstractmethod
    def extract(cls, *args, **kwargs):
        raise NotImplementedError('Need to implement `extract`.')


class DocumentMetadata(DocumentComponent):

    RECORDS = (
        RecordTemplate(
            key='target',
            pat=re.compile(r'^TARGET.*'),
            fmt=as_is
        ),
        RecordTemplate(
            key='buyer',
            pat=re.compile(r'^BUYER.*'),
            fmt=as_is
        ),
        RecordTemplate(
            key='announce_date',
            pat=re.compile(r'^ANNOUNCE\sDATE.*'),
            fmt=as_datetime
        ),
        RecordTemplate(
            key='deal_number',
            pat=re.compile(r'^DEAL\sNO.*'),
            fmt=as_int
        )
    )

    @classmethod
    def extract(cls, root_tag):
        result = {}
        for key, pat, fmt in cls.RECORDS:
            value = find_tag_by_label(root_tag, pat)
            if value is not None:
                result[key] = fmt(value.text)
            else:
                result[key] = None
        return result


class BuyerDetails(DocumentComponent):

    PATTERN = re.compile(r'.*BUYER\sDETAILS.*')
    RECORDS = (
        RowRecordTemplate(
            key='legal_status',
            pat=re.compile(r'^Legal\sStatus.*'),
            fmt=as_str
        ),
        RowRecordTemplate(
            key='primary_industry',
            pat=re.compile(r'^Primary\sIndustry.*'),
            fmt=as_is
        ),
        RowRecordTemplate(
            key='exchange',
            pat=re.compile(r'^Exchange.*'),
            fmt=as_is
        ),
        RowRecordTemplate(
            key='ticker',
            pat=re.compile(r'^Ticker.*'),
            fmt=as_is
        )
    )

    @classmethod
    def extract(cls, root_tag):
        raw_table = find_table_by_header(root_tag, cls.PATTERN)
        return extract_table(raw_table, cls.RECORDS)


class FinancialSummary(DocumentComponent):

    PATTERN = re.compile(r'.*FINANCIAL\sSUMMARY.*')
    RECORDS = (
        RowRecordTemplate(
            key='total_invested_capital_over_ebitda',
            pat=re.compile(r'^Total\sInvested\sCapital/EBITDA.*'),
            fmt=as_float
        ),
        RowRecordTemplate(
            key='total_assets',
            pat=re.compile(r'^Total\sAssets.*'),
            fmt=as_currency
        ),
        RowRecordTemplate(
            key='cash_and_marketable_securities',
            pat=re.compile(r'^Cash\sand\sMarketable\sSecurities.*'),
            fmt=as_currency
        ),
        RowRecordTemplate(
            key='current_long_term_debt',
            pat=re.compile(r'^Current\sLong\sTerm\sDebt.*'),
            fmt=as_currency
        ),
        RowRecordTemplate(
            key='long_term_debt',
            pat=re.compile(r'^Long-Term\sDebt.*'),
            fmt=as_currency
        ),
        RowRecordTemplate(
            key='book_value',
            pat=re.compile(r'^Book\sValue.*'),
            fmt=as_currency
        ),
        RowRecordTemplate(
            key='share_price_30_days_prior',
            pat=re.compile(r'^Share\sPrice\s30\sDays\sPrior.*'),
            fmt=as_currency
        ),
        RowRecordTemplate(
            key='share_price_5_days_prior',
            pat=re.compile(r'^Share\sPrice\s5\sDays\sPrior.*'),
            fmt=as_currency
        ),
        RowRecordTemplate(
            key='share_price_1_day_prior',
            pat=re.compile(r'^Share\sPrice\s1\sDay\sPrior.*'),
            fmt=as_currency
        )
    )

    @classmethod
    def extract(cls, root_tag):
        raw_table = find_table_by_first_row(root_tag, cls.PATTERN)
        return extract_table(raw_table, cls.RECORDS)


class LatestTwelveMonths(DocumentComponent):

    PATTERN = re.compile(r'.*LATEST\sTWELVE\sMONTHS.*')
    RECORDS = (
        RowRecordTemplate(
            key='units',
            pat=re.compile(r'^\('),
            fmt=as_units,
            out_col=0
        ),
        RowRecordTemplate(
            key='revenue',
            pat=re.compile(r'^Revenue.*'),
            fmt=as_currency
        ),
        RowRecordTemplate(
            key='net_income',
            pat=re.compile(r'^Net\sIncome.*'),
            fmt=as_currency
        )
    )

    @classmethod
    def extract(cls, root_tag):
        raw_table = find_table_by_first_row(root_tag, cls.PATTERN)
        return extract_table(raw_table, cls.RECORDS)


class SellerDetails(DocumentComponent):

    PATTERN = re.compile(r'.*SELLER\sDETAILS.*')
    RECORDS = (
        RowRecordTemplate(
            key='ticker',
            pat=re.compile(r'^Ticker.*'),
            fmt=as_is
        ),
    )

    @classmethod
    def extract(cls, root_tag):
        raw_table = find_table_by_header(root_tag, cls.PATTERN)
        return extract_table(raw_table, cls.RECORDS)


class TargetDetails(DocumentComponent):

    PATTERN = re.compile(r'.*TARGET\sDETAILS.*')
    RECORDS = (
        RowRecordTemplate(
            key='country',
            pat=re.compile(r'^Country.*'),
            fmt=as_is
        ),
        RowRecordTemplate(
            key='exchange',
            pat=re.compile(r'^Exchange.*'),
            fmt=as_is
        ),
        RowRecordTemplate(
            key='industry',
            pat=re.compile(r'^Industry.*'),
            fmt=as_is
        )
    )

    @classmethod
    def extract(cls, root_tag):
        raw_table = find_table_by_header(root_tag, cls.PATTERN)
        return extract_table(raw_table, cls.RECORDS)


class TransactionSummary(DocumentComponent):

    PATTERN = re.compile(r'.*TRANSACTION\sSUMMARY.*')
    RECORDS = (
        RowRecordTemplate(
            key='deal_type',
            pat=re.compile(r'^Deal\sType.*'),
            fmt=as_str
        ),
        RowRecordTemplate(
            key='purpose',
            pat=re.compile(r'^Purpose.*'),
            fmt=as_str
        ),
        RowRecordTemplate(
            key='attitude',
            pat=re.compile(r'^Attitude.*'),
            fmt=as_str
        ),
        RowRecordTemplate(
            key='transaction_type',
            pat=re.compile(r'^Transaction\sType.*'),
            fmt=as_is
        ),
        RowRecordTemplate(
            key='cancelled_date',
            pat=re.compile(r'^Cancelled\sDate.*'),
            fmt=as_datetime
        ),
        RowRecordTemplate(
            key='closing_date',
            pat=re.compile(r'^Closing\sDate.*'),
            fmt=as_datetime
        ),
        RowRecordTemplate(
            key='deal_description',
            pat=re.compile(r'^Deal\sDescription.*'),
            fmt=as_is
        ),
        RowRecordTemplate(
            key='transaction_notes',
            pat=re.compile(r'^Transaction\sNotes.*'),
            fmt=as_is
        ),
        RowRecordTemplate(
            key='method_of_payment',
            pat=re.compile(r'^Method\sof\sPayment.*'),
            fmt=as_str
        ),
        RowRecordTemplate(
            key='premium_offered',
            pat=re.compile(r'^Premium\sOffered.*'),
            fmt=as_float
        ),
        RowRecordTemplate(
            key='percent_sought',
            pat=re.compile(r'^Percent\sSought.*'),
            fmt=as_float
        ),
        RowRecordTemplate(
            key='share_price',
            pat=re.compile(r'^Share\sPrice.*'),
            fmt=as_currency
        ),
        RowRecordTemplate(
            key='original_offer_price',
            pat=re.compile(r'^Original\sOffer\sPrice.*'),
            fmt=as_currency
        ),
        RowRecordTemplate(
            key='price_earnings',
            pat=re.compile(r'^Price/Earnings.*'),
            fmt=as_float
        ),
        RowRecordTemplate(
            key='multiple_of_book_value',
            pat=re.compile(r'^Multiple\sof\sBook\sValue.*'),
            fmt=as_float
        ),
        RowRecordTemplate(
            key='stock_payment',
            pat=re.compile(r'^Stock\sPayment.*'),
            fmt=as_currency
        ),
        RowRecordTemplate(
            key='cash_payment',
            pat=re.compile(r'^Cash\sPayment.*'),
            fmt=as_currency
        ),
        RowRecordTemplate(
            key='liabilities_assumed',
            pat=re.compile(r'^Liabilities\sAssumed.*'),
            fmt=as_currency
        ),
        RowRecordTemplate(
            key='total_invested_capital',
            pat=re.compile(r'^Total\sInvested\sCapital.*'),
            fmt=as_currency
        ),
        RowRecordTemplate(
            key='stock_exchange_ratio',
            pat=re.compile(r'^Stock\sExchange\sRatio.*'),
            fmt=as_float
        ),
        RowRecordTemplate(
            key='base_equity',
            pat=re.compile(r'^Base\sEquity\sPrice.*'),
            fmt=as_currency
        ),
        RowRecordTemplate(
            key='seller_breakup_fee',
            pat=re.compile(r'^Seller\sBreakup\sFee.*'),
            fmt=as_currency
        )
    )

    @classmethod
    def extract(cls, root_tag):
        raw_table = find_table_by_header(root_tag, cls.PATTERN)
        return extract_table(raw_table, cls.RECORDS)

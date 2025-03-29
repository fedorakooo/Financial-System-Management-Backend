from enum import Enum


class LoanTermMonths(Enum):
    THREE = 3
    SIX = 6
    TWELVE = 12
    TWENTY_FOUR = 24
    THIRTY_SIX = 36
    FORTY_EIGHT = 48


class LoanTransactionType(Enum):
    CREDIT = 'CREDIT'
    PAYMENT = 'PAYMENT'

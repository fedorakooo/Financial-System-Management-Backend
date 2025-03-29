from enum import Enum


class WithdrawalSource(Enum):
    CARD_PAYMENT = "CARD_PAYMENT"
    CASH = "CASH"
    CRYPTO = "CRYPTO"
    OTHER = "OTHER"

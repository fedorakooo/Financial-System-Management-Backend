from decimal import Decimal


class PaymentError(Exception):
    """Base exception for payment handlers."""
    pass


class PaymentExceedsLimitError(PaymentError):
    """Exception raised when a payment exceeds the allowed limit."""

    def __init__(
            self,
            payment_amount: Decimal,
            max_allowed: Decimal,
            already_paid: Decimal
    ):
        self.payment_amount = payment_amount
        self.max_allowed = max_allowed
        self.already_paid = already_paid

        super().__init__(
            f"Payment of {self.payment_amount} exceeds the allowed limit. "
            f"Already paid: {self.already_paid}. "
            f"Maximum allowed payment: {self.max_allowed}"
        )

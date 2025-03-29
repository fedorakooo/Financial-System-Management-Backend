from decimal import Decimal


class LoanError(Exception):
    """Base exception for loan handlers."""
    pass


class LoanAccountNotPendingError(LoanError):
    def __init__(self):
        super().__init__(
            "The loan account is not in pending status."
        )


class LoanAccountNonZeroBalanceError(LoanError):
    def __init__(self, current_balance: Decimal):
        super().__init__(
            f"Account balance must be 0 to close the account. Current balance: : {current_balance}"
        )


class LoanError(Exception):
    """Base exception for loan-related errors."""
    pass


class InsufficientFundsError(LoanError):
    def __init__(
            self,
            current_balance: Decimal,
            required_amount: Decimal,
    ):
        self.current_balance = current_balance
        self.required_amount = required_amount
        self.message = (
            f"Insufficient funds in account for this transaction. Current balance: {current_balance}, Required amount: {required_amount}"
        )
        super().__init__(self.message)

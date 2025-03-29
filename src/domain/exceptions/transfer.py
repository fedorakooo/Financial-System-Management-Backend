from decimal import Decimal


class TransferError(Exception):
    """Base exception for transfer handlers."""
    pass

class TransferAlreadyCanceledError(TransferError):
    """Exception raised when attempting to modify an already canceled transfer."""

    def __init__(self, transfer_id: int, current_status: str):
        self.transfer_id = transfer_id
        self.current_status = current_status
        super().__init__(
            f"Transfer {transfer_id} is already canceled (current status: {current_status}). "
        )

class InsufficientRecipientBalanceError(TransferError):
    """Exception raised when recipient account has insufficient balance to complete the operation."""

    def __init__(self, account_id: int, current_balance: Decimal, required_amount: Decimal):
        self.account_id = account_id
        self.current_balance = current_balance
        self.required_amount = required_amount
        super().__init__(
            f"Recipient account {account_id} has insufficient balance. "
            f"Current balance: {current_balance}, required: {required_amount}"
        )
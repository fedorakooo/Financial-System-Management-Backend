from abc import abstractmethod, ABC

from src.application.dtos.bank import BankReadDTO, BankCreateDTO, BankUpdateDTO
from src.application.dtos.loan import LoanAccountReadDTO
from src.application.dtos.user import UserAccessDTO


class AbstractLoanManagementService(ABC):
    """Abstract service for staff-level users to manage loan."""

    @abstractmethod
    async def approve_loan_account_request(
            self,
            loan_account_id: int,
            requesting_user: UserAccessDTO
    ) -> LoanAccountReadDTO:
        """Issues the loan principal, activates its account, and records CREDIT atomically.

        Raises:
            ForbiddenError: If the staff member cannot approve loans.
            NotFoundError: If the loan or account does not exist.
            LoanAccountNotPendingError: If the account is not pending or credit was already issued.
        """
        pass
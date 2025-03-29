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
        pass
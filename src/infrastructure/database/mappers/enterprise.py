from src.domain.entities.enterprise import (
    Enterprise,
    EnterpriseSpecialist,
    EnterprisePayrollRequest,
    EnterprisePayrollTransaction
)

class EnterpriseDatabaseMapper:
    """Utility class for mapping between database rows and Enterprise entities."""

    @staticmethod
    def from_db_row_to_enterprise(row: dict) -> Enterprise:
        return Enterprise(
            id=row["id"],
            name=row["name"],
            type=row["type"],
            unp=row["unp"],
            bank_id=row["bank_id"],
            address=row["address"],
            account_id=row["account_id"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )

    @staticmethod
    def from_db_row_to_enterprise_specialist(row: dict) -> EnterpriseSpecialist:
        return EnterpriseSpecialist(
            id=row["id"],
            user_id=row["user_id"],
            enterprise_id=row["enterprise_id"]
        )

    @staticmethod
    def from_db_row_to_enterprise_payroll_request(row: dict) -> EnterprisePayrollRequest:
        return EnterprisePayrollRequest(
            id=row["id"],
            status=row["status"],
            passport_numbers=row["passport_numbers"],
            enterprise_id=row["enterprise_id"],
            specialist_id=row["specialist_id"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            amount=row["amount"]
        )

    @staticmethod
    def from_db_row_to_enterprise_payroll_transaction(row: dict) -> EnterprisePayrollTransaction:
        return EnterprisePayrollTransaction(
            payroll_request_id=row["payroll_request_id"],
            created_at=row["created_at"]
        )

    @staticmethod
    def from_enterprise_to_db_row(enterprise: Enterprise) -> dict:
        return {
            "name": enterprise.name,
            "type": enterprise.type.value,
            "unp": enterprise.unp,
            "bank_id": enterprise.bank_id,
            "address": enterprise.address,
            "account_id": enterprise.account_id,
        }

    @staticmethod
    def from_enterprise_specialist_to_db_row(enterprise_specialist: EnterpriseSpecialist) -> dict:
        return {
            "user_id": enterprise_specialist.user_id,
            "enterprise_id": enterprise_specialist.enterprise_id
        }

    @staticmethod
    def from_enterprise_payroll_request_to_db_row(enterprise_payroll_request: EnterprisePayrollRequest) -> dict:
        return {
            "status": enterprise_payroll_request.status,
            "passport_numbers": enterprise_payroll_request.passport_numbers,
            "enterprise_id": enterprise_payroll_request.enterprise_id,
            "specialist_id": enterprise_payroll_request.specialist_id,
        }

    @staticmethod
    def from_enterprise_payroll_transaction_to_db_row(enterprise_payroll_transaction: EnterprisePayrollTransaction) -> dict:
        return {
            "payroll_request_id": enterprise_payroll_transaction.payroll_request_id,
        }

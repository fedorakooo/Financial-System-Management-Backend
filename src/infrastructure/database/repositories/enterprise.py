from typing import Any

from src.domain.abstractions.database.repositories.enterprise import AbstractEnterpriseRepository
from src.domain.enums.enterprise import EnterprisePayrollRequestStatus
from src.domain.entities.enterprise import (
    Enterprise,
    EnterpriseSpecialist,
    EnterprisePayrollRequest,
    EnterprisePayrollTransaction
)
from src.infrastructure.database.mappers.enterprise import EnterpriseDatabaseMapper
from src.infrastructure.exceptions.repository_exceptions import NotFoundError


class EnterpriseRepository(AbstractEnterpriseRepository):
    def __init__(self, connection: Any):
        self.connection = connection

    async def get_enterprise_by_id(self, enterprise_id: int) -> Enterprise:
        stmt = "SELECT * FROM enterprises WHERE id = $1"
        row = await self.connection.fetchrow(stmt, enterprise_id)
        if row is None:
            raise NotFoundError(f"Enterprise with id = {enterprise_id} not found")
        return EnterpriseDatabaseMapper.from_db_row_to_enterprise(row)

    async def get_enterprise_specialist_by_user_id(self, user_id: int) -> EnterpriseSpecialist:
        stmt = "SELECT * FROM enterprise_specialists WHERE user_id = $1"
        row = await self.connection.fetchrow(stmt, user_id)
        if row is None:
            raise NotFoundError(f"Enterprise specialist with user_id = {user_id} not found")
        return EnterpriseDatabaseMapper.from_db_row_to_enterprise_specialist(row)

    async def get_enterprise_specialist_by_id(self, specialist_id: int) -> EnterpriseSpecialist:
        stmt = "SELECT * FROM enterprise_specialists WHERE id = $1"
        row = await self.connection.fetchrow(stmt, specialist_id)
        if row is None:
            raise NotFoundError(f"Enterprise specialist with id = {specialist_id} not found")
        return EnterpriseDatabaseMapper.from_db_row_to_enterprise_specialist(row)

    async def get_enterprise_payroll_request_by_id(self, enterprise_payroll_request_id: int) -> EnterprisePayrollRequest:
        stmt = "SELECT * FROM enterprise_payroll_requests WHERE id = $1"
        row = await self.connection.fetchrow(stmt, enterprise_payroll_request_id)
        if row is None:
            raise NotFoundError(f"Enterprise payroll request with id = {enterprise_payroll_request_id} not found")
        return EnterpriseDatabaseMapper.from_db_row_to_enterprise_payroll_request(row)

    async def create_enterprise_specialist(self, enterprise_specialist: EnterpriseSpecialist) -> EnterpriseSpecialist:
        data = EnterpriseDatabaseMapper.from_enterprise_specialist_to_db_row(enterprise_specialist)
        columns = ', '.join(data.keys())
        placeholders = ', '.join([f"${i + 1}" for i in range(len(data))])
        values = tuple(data.values())
        stmt = f"INSERT INTO enterprise_specialists ({columns}) VALUES ({placeholders}) RETURNING *"
        row = await self.connection.fetchrow(stmt, *values)
        return EnterpriseDatabaseMapper.from_db_row_to_enterprise_specialist(row)

    async def get_enterprise_payroll_transactions_by_payroll_request_id(
            self, enterprise_payroll_request_id: int
    ) -> list[EnterprisePayrollTransaction]:
        stmt = "SELECT * FROM enterprise_payroll_transactions WHERE payroll_request_id = $1"
        rows = await self.connection.fetch(stmt, enterprise_payroll_request_id)
        return [EnterpriseDatabaseMapper.from_db_row_to_enterprise_payroll_transaction(row) for row in rows]

    async def create_payroll_request(self, payroll_request: EnterprisePayrollRequest) -> EnterprisePayrollRequest:
        data = EnterpriseDatabaseMapper.from_enterprise_payroll_request_to_db_row(payroll_request)
        columns = ', '.join(data.keys())
        placeholders = ', '.join([f"${i + 1}" for i in range(len(data))])
        values = tuple(data.values())
        stmt = f"INSERT INTO enterprise_payroll_requests ({columns}) VALUES ({placeholders}) RETURNING *"
        row = await self.connection.fetchrow(stmt, *values)
        return EnterpriseDatabaseMapper.from_db_row_to_enterprise_payroll_request(row)

    async def create_enterprise_payroll_transaction(
            self, enterprise_payroll_transaction: EnterprisePayrollTransaction
    ) -> EnterprisePayrollTransaction:
        data = EnterpriseDatabaseMapper.from_enterprise_payroll_transaction_to_db_row(enterprise_payroll_transaction)
        columns = ', '.join(data.keys())
        placeholders = ', '.join([f"${i + 1}" for i in range(len(data))])
        values = tuple(data.values())
        stmt = f"INSERT INTO enterprise_payroll_transactions ({columns}) VALUES ({placeholders}) RETURNING *"
        row = await self.connection.fetchrow(stmt, *values)
        return EnterpriseDatabaseMapper.from_db_row_to_enterprise_payroll_transaction(row)

    async def create_enterprise(self, enterprise: Enterprise) -> Enterprise:
        data = EnterpriseDatabaseMapper.from_enterprise_to_db_row(enterprise)
        columns = ', '.join(data.keys())
        placeholders = ', '.join([f"${i + 1}" for i in range(len(data))])
        values = tuple(data.values())
        stmt = f"INSERT INTO enterprises ({columns}) VALUES ({placeholders}) RETURNING *"
        row = await self.connection.fetchrow(stmt, *values)
        return EnterpriseDatabaseMapper.from_db_row_to_enterprise(row)

    async def update_payroll_request_status_by_id(
            self, payroll_request_id: int, payroll_request_status: EnterprisePayrollRequestStatus
    ) -> EnterprisePayrollRequest:
        stmt = "UPDATE enterprise_payroll_requests SET status = $1 WHERE id = $2 RETURNING *"
        row = await self.connection.fetchrow(stmt, payroll_request_status.value, payroll_request_id)
        if row is None:
            raise NotFoundError(f"Enterprise payroll request with id = {payroll_request_id} not found")
        return EnterpriseDatabaseMapper.from_db_row_to_enterprise_payroll_request(row)

from src.domain.abstractions.database.connection import AbstractDatabaseConnection


class DatabaseInitializer:
    """Class responsible for initializing the database by creating all necessary tables and database objects (e.g., enums, triggers)."""

    def __init__(self, db_connection: AbstractDatabaseConnection):
        self.db_connection = db_connection

    async def create_all_tables(self) -> None:
        """Method to call the creation of all tables"""
        await self.create_banks_table()
        await self.create_users_table()
        await self.create_accounts_table()
        await self.create_additions_table()
        await self.create_withdrawals_table()
        await self.create_transfers_table()
        await self.create_loans_table()
        await self.create_deposits_table()
        await self.create_enterprise_tables()

    async def create_banks_table(self) -> None:
        create_table = """
            CREATE TABLE IF NOT EXISTS banks (
                id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                name VARCHAR(150) NOT NULL,
                bic VARCHAR(32) NOT NULL UNIQUE,
                address VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT now() NOT NULL,
                updated_at TIMESTAMP DEFAULT now() NOT NULL
            );
        """

        create_index = "CREATE INDEX IF NOT EXISTS idx_banks_bic ON banks(bic);"

        create_function = """
            CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = now();
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """

        create_trigger = """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'trigger_update_updated_at') THEN
                    CREATE TRIGGER trigger_update_updated_at
                    BEFORE UPDATE ON banks
                    FOR EACH ROW
                    EXECUTE FUNCTION update_updated_at_column();
                END IF;
            END $$;
        """

        async with self.db_connection as conn:
            await conn.execute(create_table)
            await conn.execute(create_index)
            await conn.execute(create_function)
            await conn.execute(create_trigger)

    async def create_users_table(self) -> None:
        create_enum_role = """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role') THEN
                    CREATE TYPE user_role AS ENUM ('CLIENT', 'OPERATOR', 'MANAGER', 'ADMINISTRATOR', 'SPECIALIST');
                END IF;
            END $$;
        """

        create_table = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                name VARCHAR(150) NOT NULL,
                passport_number VARCHAR(20) NOT NULL UNIQUE,
                phone_number VARCHAR(20) NOT NULL UNIQUE,
                email VARCHAR(100) NOT NULL UNIQUE,
                role user_role NOT NULL,
                hashed_password TEXT NOT NULL,
                is_active BOOLEAN NOT NULL DEFAULT FALSE,
                is_foreign BOOLEAN NOT NULL DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
            );
        """

        create_function = """
            CREATE OR REPLACE FUNCTION update_user_updated_at()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = now();
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """

        create_trigger = """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'trigger_update_user_updated_at') THEN
                    CREATE TRIGGER trigger_update_user_updated_at
                    BEFORE UPDATE ON users
                    FOR EACH ROW
                    EXECUTE FUNCTION update_user_updated_at();
                END IF;
            END $$;
        """

        async with self.db_connection as conn:
            await conn.execute(create_enum_role)
            await conn.execute(create_table)
            await conn.execute(create_function)
            await conn.execute(create_trigger)

    async def create_accounts_table(self) -> None:
        create_enum_status = """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'account_status') THEN
                    CREATE TYPE account_status AS ENUM ('ACTIVE', 'BLOCKED', 'FROZEN', 'ON_CONSIDERATION');
                END IF;
            END $$;
        """

        create_enum_type = """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'account_type') THEN
                    CREATE TYPE account_type AS ENUM ('SALARY', 'DEPOSIT', 'LOAN', 'SETTLEMENT', 'ENTERPRISE');
                END IF;
            END $$;
        """

        create_table = """
            CREATE TABLE IF NOT EXISTS accounts (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id),
                bank_id INTEGER NOT NULL REFERENCES banks(id),
                balance DECIMAL(30,2) NOT NULL CHECK (balance >= 0) DEFAULT 0,
                status account_status NOT NULL DEFAULT 'ON_CONSIDERATION',
                type account_type NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """

        create_function = """
            CREATE OR REPLACE FUNCTION update_account_updated_at()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = now();
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """

        create_trigger = """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'trigger_update_account_updated_at') THEN
                    CREATE TRIGGER trigger_update_account_updated_at
                    BEFORE UPDATE ON accounts
                    FOR EACH ROW
                    EXECUTE FUNCTION update_account_updated_at();
                END IF;
            END $$;
        """

        async with self.db_connection as conn:
            await conn.execute(create_enum_status)
            await conn.execute(create_enum_type)
            await conn.execute(create_table)
            await conn.execute(create_function)
            await conn.execute(create_trigger)

    async def create_additions_table(self) -> None:
        create_enum_source = """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'addition_source') THEN
                    CREATE TYPE addition_source AS ENUM ('BANK_TRANSFER', 'CARD_PAYMENT', 'CASH', 'CRYPTO', 'OTHER');
                END IF;
            END $$;
        """

        create_table = """
            CREATE TABLE IF NOT EXISTS additions (
                id SERIAL PRIMARY KEY,
                account_id BIGINT NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
                amount DECIMAL(18,2) NOT NULL CHECK (amount >= 0),
                source addition_source NOT NULL,
                created_at TIMESTAMP DEFAULT NOW() NOT NULL
            );
        """

        async with self.db_connection as conn:
            await conn.execute(create_enum_source)
            await conn.execute(create_table)

    async def create_withdrawals_table(self) -> None:
        create_enum_source = """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'withdrawal_source') THEN
                    CREATE TYPE withdrawal_source AS ENUM ('BANK_TRANSFER', 'CARD_PAYMENT', 'CASH', 'CRYPTO', 'OTHER');
                END IF;
            END $$;
        """

        create_table = """
            CREATE TABLE IF NOT EXISTS withdrawals (
                id SERIAL PRIMARY KEY,
                account_id BIGINT NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
                amount DECIMAL(18,2) NOT NULL CHECK (amount >= 0),
                source withdrawal_source NOT NULL,
                created_at TIMESTAMP DEFAULT NOW() NOT NULL
            );
        """

        async with self.db_connection as conn:
            await conn.execute(create_enum_source)
            await conn.execute(create_table)

    async def create_transfers_table(self) -> None:
        create_enum_status = """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'transfer_status') THEN
                    CREATE TYPE transfer_status AS ENUM ('COMPLETED', 'CANCELED');
                END IF;
            END $$;
        """

        create_table = """
            CREATE TABLE IF NOT EXISTS transfers (
                id SERIAL PRIMARY KEY,
                from_account_id BIGINT NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
                to_account_id BIGINT NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
                amount DECIMAL(18,2) NOT NULL CHECK (amount > 0),
                status transfer_status NOT NULL DEFAULT 'COMPLETED',
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP NOT NULL DEFAULT NOW() 
            );
        """

        create_function = """
            CREATE OR REPLACE FUNCTION update_transfer_updated_at()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = now();
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """

        create_trigger = """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'trigger_update_transfer_updated_at') THEN
                    CREATE TRIGGER trigger_update_transfer_updated_at
                    BEFORE UPDATE ON transfers
                    FOR EACH ROW
                    EXECUTE FUNCTION update_transfer_updated_at();
                END IF;
            END $$;
        """

        async with self.db_connection as conn:
            await conn.execute(create_enum_status)
            await conn.execute(create_table)
            await conn.execute(create_function)
            await conn.execute(create_trigger)

    async def create_loans_table(self) -> None:
        create_enum_loan_transaction_type = """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'loan_transaction_type') THEN
                    CREATE TYPE loan_transaction_type AS ENUM ('CREDIT', 'PAYMENT');
                END IF;
            END $$;
        """

        create_loans_table = """
            CREATE TABLE IF NOT EXISTS loans (
                id SERIAL PRIMARY KEY,
                amount DECIMAL(18,2) NOT NULL,
                term_months BIGINT,
                interest_rate DECIMAL(5,2) NOT NULL,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
        """

        create_loan_accounts_table = """
            CREATE TABLE IF NOT EXISTS loan_accounts (
                id SERIAL PRIMARY KEY,
                account_id BIGINT NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
                loan_id BIGINT NOT NULL REFERENCES loans(id) ON DELETE CASCADE,
                user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE
            );
        """

        create_loan_transactions_table = """
            CREATE TABLE IF NOT EXISTS loan_transactions (
                id SERIAL PRIMARY KEY,
                loan_account_id BIGINT NOT NULL REFERENCES loan_accounts(id) ON DELETE CASCADE,
                type loan_transaction_type NOT NULL,
                amount DECIMAL(18 ,2) NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
        """

        create_trigger = """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'trigger_update_loan_updated_at') THEN
                    CREATE TRIGGER trigger_update_loan_updated_at
                    BEFORE UPDATE ON loans
                    FOR EACH ROW
                    EXECUTE FUNCTION update_loan_updated_at();
                END IF;
            END $$;
        """

        create_function = """
            CREATE OR REPLACE FUNCTION update_loan_updated_at()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = now();
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """

        async with self.db_connection as conn:
            await conn.execute(create_enum_loan_transaction_type)
            await conn.execute(create_loans_table)
            await conn.execute(create_loan_accounts_table)
            await conn.execute(create_loan_transactions_table)
            await conn.execute(create_function)
            await conn.execute(create_trigger)

    async def create_deposits_table(self) -> None:
        create_enum_deposit_transaction_type = """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'deposit_transaction_type') THEN
                    CREATE TYPE deposit_transaction_type AS ENUM ('DEPOSIT', 'WITHDRAWAL');
                END IF;
            END $$;
        """

        create_deposit_accounts_table = """
            CREATE TABLE IF NOT EXISTS deposit_accounts (
                id SERIAL PRIMARY KEY,
                account_id BIGINT NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
                interest_rate DECIMAL(5,2),
                from_account_id BIGINT NOT NULL REFERENCES accounts(id),
                user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE
            );
        """

        create_deposit_transactions_table = """
            CREATE TABLE IF NOT EXISTS deposit_transactions (
                id SERIAL PRIMARY KEY,
                deposit_account_id BIGINT NOT NULL REFERENCES deposit_accounts(id) ON DELETE CASCADE,
                account_id BIGINT NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
                type deposit_transaction_type NOT NULL,
                amount DECIMAL(18 ,2) NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
        """

        async with self.db_connection as conn:
            await conn.execute(create_enum_deposit_transaction_type)
            await conn.execute(create_deposit_accounts_table)
            await conn.execute(create_deposit_transactions_table)

    async def create_enterprise_tables(self) -> None:
        create_enum_enterprise_type = """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'enterprise_type') THEN
                    CREATE TYPE enterprise_type AS ENUM ('LLC', 'SP', 'LLP');
                END IF;
            END $$;
        """

        create_enum_payroll_request_status = """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'enterprise_payroll_request_status') THEN
                    CREATE TYPE enterprise_payroll_request_status AS ENUM ('ON_CONSIDERATION', 'CANCELLED', 'APPROVED');
                END IF;
            END $$;
        """

        create_enterprise_table = """
            CREATE TABLE IF NOT EXISTS enterprises (
                id BIGSERIAL PRIMARY KEY,
                name VARCHAR NOT NULL,
                type enterprise_type NOT NULL,
                unp VARCHAR NOT NULL,
                bank_id BIGINT NOT NULL REFERENCES banks(id) ON DELETE CASCADE,
                address VARCHAR NOT NULL,
                account_id BIGINT NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            );
        """

        create_enterprise_specialists_table = """
            CREATE TABLE IF NOT EXISTS enterprise_specialists (
                id BIGSERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                enterprise_id BIGINT NOT NULL REFERENCES enterprises(id) ON DELETE CASCADE
            );
        """

        create_enterprise_payroll_requests_table = """
            CREATE TABLE IF NOT EXISTS enterprise_payroll_requests (
                id BIGSERIAL PRIMARY KEY,
                status enterprise_payroll_request_status NOT NULL,
                passport_numbers TEXT[] NOT NULL,
                accounts_id BIGINT[] NOT NULL,
                enterprise_id BIGINT NOT NULL REFERENCES enterprises(id) ON DELETE CASCADE,
                specialist_id BIGINT NOT NULL REFERENCES enterprise_specialists(id) ON DELETE CASCADE,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            );
        """

        create_enterprise_payroll_transactions_table = """
            CREATE TABLE IF NOT EXISTS enterprise_payroll_transactions (
                id BIGSERIAL PRIMARY KEY,
                enterprise_payroll_request_id BIGINT NOT NULL REFERENCES enterprise_payroll_requests(id) ON DELETE CASCADE,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """

        async with self.db_connection as conn:
            await conn.execute(create_enum_enterprise_type)
            await conn.execute(create_enum_payroll_request_status)
            await conn.execute(create_enterprise_table)
            await conn.execute(create_enterprise_specialists_table)
            await conn.execute(create_enterprise_payroll_requests_table)
            await conn.execute(create_enterprise_payroll_transactions_table)

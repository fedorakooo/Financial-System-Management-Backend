# Financial System Management Backend

A FastAPI backend for bank accounts, transfers, deposits, loans and enterprise payroll. Clients manage their own accounts. Staff manage banks and users, approve requests and reverse transfers. Enterprise specialists submit and pay payroll requests.

The code runs on Python 3.11 with FastAPI 0.115.8 and PostgreSQL 16.8.

## Running it

You'll need Docker Engine, Docker Compose and OpenSSL. For the local Python setup, use Python 3.11.

```bash
git clone https://github.com/fedorakooo/Financial-System-Management-Backend.git
cd Financial-System-Management-Backend
```

Create `.env` in the project root:

```dotenv
DB_HOST=database
DB_PORT=5432
DB_USER=financial
DB_PASS=your_database_password
DB_NAME=financial
```

Replace `your_database_password` with your local database password. `DB_USER`, `DB_PASS` and `DB_NAME` are also used to initialize the PostgreSQL container.

### JWT keys

The app reads its key files during import, so create them before starting it. If you already have a key pair, keep it rather than running these commands again:

```bash
mkdir -p certs
umask 077
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out certs/jwt-private.pem
openssl pkey -in certs/jwt-private.pem -pubout -out certs/jwt-public.pem
```

The paths are set in [`config.yml`](config.yml), relative to the project root. Tokens use RS256 and expire after 120 minutes by default. Compose mounts `./certs` read-only inside the backend container.

### Start with Compose

```bash
docker compose up --build -d
```

Compose waits for the PostgreSQL health check before starting the backend. Wait for `Application startup complete` in the backend logs before sending requests.

| Service | Address |
| --- | --- |
| Backend | [http://localhost:8000](http://localhost:8000) |
| Swagger UI | [http://localhost:8000/docs](http://localhost:8000/docs) |
| ReDoc | [http://localhost:8000/redoc](http://localhost:8000/redoc) |
| OpenAPI schema | [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json) |
| PostgreSQL | `localhost:5432` |

To check the containers, follow the backend logs or stop the stack:

```bash
docker compose ps
docker compose logs -f backend
docker compose down
```

### Run Python locally

Use the same `.env` and JWT keys. Run this from the repository root:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Keep PostgreSQL in Docker and release the backend's port if it is running.
docker compose stop backend
docker compose up -d database

DB_HOST=127.0.0.1 uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
```

This keeps PostgreSQL in Docker and runs the backend locally. If you're using another PostgreSQL server, create its user and database first and update `.env`. The app creates tables, not the database itself.

## Users and roles

Registration creates a `CLIENT` with `is_active=false`. That user can log in, but protected requests will fail until a manager or administrator activates them through `PATCH /staff/users/{user_id}`.

| Role | Access |
| --- | --- |
| `CLIENT` | Own profile, account requests and financial operations on owned accounts. |
| `OPERATOR` | Read banks, accounts, users, transfers and enterprise information through staff routes. |
| `MANAGER` | Manage banks, accounts and users, approve loans and payroll, and reverse transfers. |
| `ADMINISTRATOR` | Staff management operations, including approvals and transfer reversals. |
| `SPECIALIST` | The associated enterprise, owned payroll requests and their payment history. |

Send the token on protected requests:

```http
Authorization: Bearer <access_token>
```

The backend reads the current role and activity from the database. Deactivating a user or changing their role takes effect on their next request, even if their token hasn't expired.

## API

These are the routes in the current app. [Swagger UI](http://localhost:8000/docs) has the request and response schemas.

### Public routes and profiles

| Method | Endpoint | Purpose                                                                              |
| --- | --- |--------------------------------------------------------------------------------------|
| `POST` | `/registration/` | Register an inactive client.                                                         |
| `POST` | `/login` | Log in using form fields `phone number` and `password`. |
| `GET` | `/banks/` | List banks.                                                                          |
| `GET` | `/banks/{bank_id}` | Read a bank.                                                                         |
| `GET`, `PATCH`, `DELETE` | `/profile/` | Read, update, or delete the authenticated user's profile.                            |

### Client accounts

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET`, `POST` | `/profile/accounts/` | List owned accounts or request a settlement account. |
| `GET`, `PATCH` | `/profile/accounts/{account_id}` | Read an owned account or request an allowed status change. |
| `GET`, `POST` | `/profile/accounts/additions/` | Read additions or add funds to a settlement account. |
| `GET`, `POST` | `/profile/accounts/withdrawals/` | Read withdrawals or withdraw settlement funds. |
| `GET`, `POST` | `/profile/accounts/transfers/` | Read transfers or send funds from an owned account. |
| `POST` | `/profile/accounts/loan_accounts/` | Submit a loan request. |
| `GET` | `/profile/accounts/loan_accounts/{account_id}` | Read loan details using the underlying bank account ID. |
| `GET`, `POST` | `/profile/accounts/loan_accounts/{loan_account_id}/transactions` | Read loan history or make a repayment. |
| `POST` | `/profile/accounts/deposit_accounts/` | Create and fund a deposit. |
| `GET`, `POST` | `/profile/accounts/deposit_accounts/{deposit_account_id}` | Read a deposit or withdraw its full balance. |

Additions, withdrawals and transfers take `account_id` as a query parameter.

### Staff

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET`, `POST` | `/staff/banks/` | List or create banks. |
| `GET`, `PATCH`, `DELETE` | `/staff/banks/{bank_id}` | Read, update, or delete a bank. |
| `GET` | `/staff/users/` | List users. |
| `GET`, `PATCH`, `DELETE` | `/staff/users/{user_id}` | Read a user, change activity, or delete a user. |
| `GET` | `/staff/accounts/` | List accounts using the `user_id` query parameter. |
| `PATCH`, `DELETE` | `/staff/accounts/{account_id}` | Change account status or delete an account. |
| `POST` | `/staff/accounts/loans/{loan_account_id}` | Approve and issue a pending loan. |
| `GET`, `POST` | `/staff/accounts/transfers/{transfer_id}` | Read or reverse a transfer. |
| `POST` | `/staff/enterprises/` | Create an enterprise and its account. |
| `GET` | `/staff/enterprises/{enterprise_id}` | Read an enterprise. |
| `GET`, `POST` | `/staff/enterprises/payroll_requests/{payroll_request_id}` | Read or approve a payroll request. |
| `POST` | `/staff/enterprises/specialist` | Create a specialist user and enterprise association. |

### Enterprise specialists

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/enterprises/specialists/profile` | Read the specialist's profile and enterprise details. |
| `POST` | `/enterprises/specialists/payroll_requests` | Submit a payroll request. |
| `GET` | `/enterprises/specialists/payroll_requests/{payroll_request_id}` | Read an owned payroll request. |
| `POST` | `/enterprises/specialists/payroll_requests/{payroll_request_id}/make` | Execute an approved payroll request. |
| `GET` | `/enterprises/specialists/payroll_transactions/{payroll_request_id}` | Read the request's payment history. |

## Examples

### Registration and login

```bash
curl -X POST http://localhost:8000/registration/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Demo Client",
    "passport_number": "MP1234567",
    "phone_number": "+375291234567",
    "email": "client@example.com",
    "password": "your_local_password",
    "is_foreign": false
  }'
```

```bash
curl -X POST http://localhost:8000/login \
  --data-urlencode "username=+375291234567" \
  --data-urlencode "password=your_local_password"
```

Login returns `access_token` and `token_type`. Once the user is active, use that token for requests:

```bash
export TOKEN="<access_token>"

curl http://localhost:8000/profile/ \
  -H "Authorization: Bearer $TOKEN"
```

### Accounts and transfers

Create a bank through the staff API first. Then, as an active client, request an account:

```bash
curl -X POST http://localhost:8000/profile/accounts/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"bank_id": 1}'
```

It starts in `ON_CONSIDERATION`. A manager or administrator activates it with `PATCH /staff/accounts/{account_id}` and `{"status": "ACTIVE"}`. A client can move an owned active account to `BLOCKED` or `FROZEN`, but can't approve it.

Use the account ID returned by the API when adding funds:

```bash
curl -X POST 'http://localhost:8000/profile/accounts/additions/?account_id=1' \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount": "100.00", "source": "CASH"}'
```

Both accounts must be active for a transfer:

```bash
curl -X POST 'http://localhost:8000/profile/accounts/transfers/?account_id=1' \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount": "25.50", "to_account_id": 2}'
```

### Loans

Send both objects to `POST /profile/accounts/loan_accounts/`:

```json
{
  "loan_create_request": {
    "amount": "1000.00",
    "term_months": 12,
    "interest_rate": "1.10"
  },
  "account_create_request": {
    "bank_id": 1
  }
}
```

`interest_rate` is a total repayment multiplier, not an annual percentage rate. Here, `1000.00 × 1.10` gives a repayment limit of `1100.00`. The result is rounded to two decimal places with `ROUND_HALF_UP`.

A manager or administrator approves the request using `loan_account_id`. Approval credits the principal and records a `CREDIT` transaction. Repayments debit the loan account and record `PAYMENT` transactions. You can transfer funds into the loan account to cover payments.

The final payment blocks the account if its balance is zero. If money would remain, that payment is rolled back.

Terms are 3, 6, 12, 24, 36 or 48 months. Watch the IDs: approval and transactions use `loan_account_id`, while the loan details endpoint takes the underlying bank account's `account_id`.

### Deposits

Send this to `POST /profile/accounts/deposit_accounts/`:

```json
{
  "deposit_create_request": {
    "amount": "250.00",
    "interest_rate": "1.05",
    "from_account_id": 1
  },
  "account_create_request": {
    "bank_id": 1
  }
}
```

The amount is taken from an owned, active settlement account in the same bank. The deposit starts in `ON_CONSIDERATION` and needs staff activation.

After activation, send `{"account_id": 1}` to `POST /profile/accounts/deposit_accounts/{deposit_account_id}`. This moves the entire balance to an owned, active settlement account and blocks the emptied deposit. The interest rate is stored, but no background interest accrual runs.

### Payroll

An active specialist can submit this to `POST /enterprises/specialists/payroll_requests`:

```json
{
  "passport_numbers": ["MP1234567", "MP7654321"],
  "amount": "500.00",
  "enterprise_id": 1,
  "specialist": 1
}
```

`specialist` is the enterprise specialist record ID. `amount` is the payment per employee.

Staff approval creates salary accounts for the registered recipients and saves their IDs. The specialist then executes the approved request once. All recipient credits, the enterprise debit and the payment record are saved in one transaction.

## Code layout

Routes and authentication dependencies are in `src/api`. Services, access checks, DTOs and their mappers are in `src/application`. Domain entities, enums, exceptions and interfaces live in `src/domain`. The database code, JWT handling, bcrypt password hashing and DI containers are in `src/infrastructure`.

```text
.
├── src/
│   ├── api/
│   │   ├── routes/              # Public, client, staff, and specialist endpoints
│   │   ├── security.py          # Current user authentication
│   │   └── startup.py           # Database initialization
│   ├── application/
│   │   ├── abstractions/        # Application service contracts
│   │   ├── dtos/                # Data transfer objects
│   │   ├── mappers/             # DTO ↔ domain mapping
│   │   └── services/            # Financial and user workflows
│   ├── domain/
│   │   ├── abstractions/        # Persistence and infrastructure contracts
│   │   ├── entities/            # Domain models
│   │   ├── enums/               # Roles, account types, and operation statuses
│   │   └── exceptions/          # Domain errors
│   ├── infrastructure/
│   │   ├── auth/                # JWT implementation
│   │   ├── database/            # Connection, repositories, mappers, and UoWs
│   │   ├── dependencies/        # Dependency Injector containers
│   │   ├── schemas/             # Pydantic request and response models
│   │   └── security/            # bcrypt password handling
│   ├── config.py
│   └── main.py                  # ASGI entry point
├── config.yml
├── docker-compose.yaml
├── Dockerfile
├── requirements.txt
└── LICENSE
```


Repositories use parameterized SQL through `asyncpg` (there's no ORM). Each Unit of Work opens its own connection and transaction, commits on success and rolls back on an exception. The connection is closed on exit. Operations that move money write their balance changes and history records in the same transaction. When several accounts are involved, they're locked in ID order.

Startup creates missing tables, enums and triggers in one transaction. An advisory lock keeps concurrent startup processes from initializing the schema at the same time. It doesn't migrate existing tables.


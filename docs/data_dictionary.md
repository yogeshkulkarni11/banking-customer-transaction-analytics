# Data Dictionary

## Customers

| Column | Type | Description |
|---|---|---|
| customer_id | string | Unique customer identifier |
| customer_name | string | Synthetic customer name |
| age | integer | Customer age |
| city | string | Customer city |
| customer_segment | string | Premium or Standard segment |
| join_date | date | Customer onboarding date |

## Accounts

| Column | Type | Description |
|---|---|---|
| account_id | string | Unique account identifier |
| customer_id | string | Customer owning the account |
| account_type | string | Savings, Current, Credit or Investment |
| opening_date | date | Account opening date |
| balance | double | Synthetic account balance |
| status | string | Account status |

## Transactions

| Column | Type | Description |
|---|---|---|
| transaction_id | string | Unique transaction identifier |
| account_id | string | Account used for transaction |
| customer_id | string | Customer initiating transaction |
| transaction_date | date | Transaction date |
| transaction_type | string | Debit or Credit |
| category | string | Business transaction category |
| amount | double | Transaction amount |
| channel | string | UPI, Card or NEFT |
| status | string | Success or Failed |

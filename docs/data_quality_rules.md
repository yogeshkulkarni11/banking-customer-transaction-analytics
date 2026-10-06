# Data Quality Rules

The pipeline uses a quality gate between Silver and Gold. The goal is to prevent invalid or inconsistent records from becoming business-facing analytics.

| Rule | Dataset | Logic | Business reason |
|---|---|---|---|
| Required fields not null | Customers | customer_id and customer_name must exist | Customer identity is mandatory |
| Required fields not null | Accounts | account_id and customer_id must exist | Account ownership must be known |
| Required fields not null | Transactions | transaction_id, account_id, customer_id and amount must exist | Transactions must be traceable |
| Primary/business key unique | All | IDs must be unique after Silver deduplication | Prevent double counting |
| Amount non-negative | Transactions | amount >= 0 | Monetary amount cannot be negative; direction is represented by transaction_type |
| Account → Customer FK | Accounts | Every account customer_id must exist in Customers | Prevent orphan accounts |
| Transaction → Account FK | Transactions | Every account_id must exist in Accounts | Ensure transaction traceability |
| Transaction → Customer FK | Transactions | Every customer_id must exist in Customers | Ensure customer traceability |
| Status domain | Transactions | Success or Failed | Standardize operational status |
| Transaction type domain | Transactions | Debit or Credit | Standardize transaction direction |
| Table not empty | Transactions | At least one record must exist | Prevent publishing an empty analytics pipeline |

## Deliberately included test scenarios

The synthetic transaction dataset includes:

- A failed transaction that is retained in Bronze/Silver but excluded from successful analytics.
- A duplicate transaction ID to demonstrate Silver deduplication.
- Multiple months of transactions to support month-over-month analytics.

## Production extension

For a production banking pipeline, extend these checks with source-to-target reconciliation totals, freshness/SLA checks, schema drift detection, anomaly thresholds, duplicate detection using composite business keys and quarantine tables for rejected records.

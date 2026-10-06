# Business Requirements

1. Ingest customer, account and transaction source files.
2. Preserve source records in Bronze with ingestion metadata.
3. Standardize dates, numeric fields and identifiers in Silver.
4. Remove duplicate primary/business keys.
5. Reject invalid transaction amounts and failed transactions from analytics.
6. Enrich transactions with customer and account attributes.
7. Produce customer 360 analytics.
8. Produce monthly transaction trends and average transaction values.
9. Rank customers by debit spending.
10. Produce account-level KPIs by account type and status.
11. Produce category-level spending analysis.
12. Execute automated data-quality checks before Gold processing.
13. Keep the pipeline executable locally and portable to Azure Databricks.

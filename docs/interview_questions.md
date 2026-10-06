# Interview Questions

### 1. Why Medallion Architecture?
Bronze preserves source fidelity, Silver creates trusted standardized data, and Gold serves business-specific analytics. It separates concerns and makes debugging and governance easier.

### 2. Why use PySpark?
PySpark provides distributed processing and scales the same transformation patterns from local samples to large datasets in Databricks.

### 3. Why filter failed transactions?
Operationally failed transactions should not contribute to successful customer spending and financial KPIs. They can be retained in Bronze for auditability.

### 4. Where are window functions used?
Customer spending uses ranking. The same pattern can be extended to running totals, latest-record selection and month-over-month calculations.

### 5. How would you productionize this?
Move data to ADLS/Delta, use Unity Catalog, add incremental processing, quarantine invalid records, parameterize environments, add observability, and orchestrate with Databricks Workflows or ADF.

### 6. How would you handle duplicate transactions?
Use transaction_id as a business key and deduplicate in Silver. For production, combine the key with source-system reconciliation rules if identifiers are not globally unique.

### 7. What belongs in Bronze?
Raw source attributes plus ingestion metadata. Business transformations should generally not destroy the original source representation.

### 8. How would you handle late-arriving data?
Use event-time processing, watermarks where appropriate, idempotent writes and controlled reprocessing of affected partitions.

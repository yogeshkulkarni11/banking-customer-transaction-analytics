# Azure Databricks Mapping

| Local Project | Azure Production Equivalent |
|---|---|
| CSV files | ADLS Gen2 landing zone |
| Bronze DataFrame | Bronze Delta table |
| Silver DataFrame | Silver Delta table |
| Gold DataFrame | Gold Delta tables/views |
| Local Spark | Azure Databricks cluster or serverless compute |
| Local filesystem | ADLS Gen2 / Unity Catalog volumes |
| pytest | CI/CD quality gate |
| Python pipeline | Databricks Workflow / ADF orchestration |
| Synthetic secrets-free data | Production governed datasets |

## Production Enhancements

- Use Delta Lake for ACID transactions and schema evolution.
- Use Unity Catalog for permissions, lineage and governance.
- Store credentials in Azure Key Vault rather than source code.
- Add incremental ingestion using checkpoints/watermarks.
- Add structured logging and operational metrics.
- Add quarantine tables for failed data-quality records.
- Parameterize storage paths and environment names.
- Schedule through Databricks Workflows or Azure Data Factory.

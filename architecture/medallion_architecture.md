# Medallion Architecture

```mermaid
flowchart TB
    S1[Customers CSV] --> B[Bronze Layer]
    S2[Accounts CSV] --> B
    S3[Transactions CSV] --> B
    B -->|schema/type validation| SIL[Silver Layer]
    SIL --> Q[Data Quality Gate]
    Q --> G1[Gold Customer 360]
    Q --> G2[Gold Monthly Trends]
    Q --> G3[Gold Spending]
    Q --> G4[Gold Account KPIs]
    Q --> G5[Gold Category Analysis]
```

## Bronze

Purpose: source preservation and ingestion observability.

Typical production format: Delta tables in ADLS Gen2.

## Silver

Purpose: clean, standardize, deduplicate and enrich data.

Transformations include type casting, date normalization, null checks, duplicate removal, failed-transaction exclusion and joins across source entities.

## Gold

Purpose: optimized business consumption.

Datasets are shaped around business questions rather than source-system structure.

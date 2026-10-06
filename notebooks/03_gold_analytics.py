from pathlib import Path
from src.utils.spark_session import get_spark
from src.bronze.ingestion import ingest_csv
from src.silver.transformations import clean_customers, clean_accounts, clean_transactions, enrich_transactions
from src.gold.analytics import customer_360, monthly_transaction_trends, customer_spending_analysis, account_kpis, category_analysis

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw"
spark = get_spark("GoldAnalytics")

customers = clean_customers(ingest_csv(spark, str(DATA / "customers.csv")))
accounts = clean_accounts(ingest_csv(spark, str(DATA / "accounts.csv")))
transactions = clean_transactions(ingest_csv(spark, str(DATA / "transactions.csv")))
enriched = enrich_transactions(transactions, accounts, customers)

for name, df in {
    "Customer 360": customer_360(customers, accounts, enriched),
    "Monthly Trends": monthly_transaction_trends(enriched),
    "Customer Spending": customer_spending_analysis(enriched),
    "Account KPIs": account_kpis(accounts),
    "Category Analysis": category_analysis(enriched),
}.items():
    print(f"\n=== {name} ===")
    df.show(20, truncate=False)

spark.stop()

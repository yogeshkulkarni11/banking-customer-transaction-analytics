from pathlib import Path

from src.utils.spark_session import get_spark
from src.bronze.ingestion import ingest_csv, add_ingestion_metadata
from src.silver.transformations import clean_customers, clean_accounts, clean_transactions, enrich_transactions
from src.gold.analytics import customer_360, monthly_transaction_trends, customer_spending_analysis, account_kpis, category_analysis
from src.quality.checks import run_quality_checks

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw"
OUTPUT = ROOT / "output"


def main():
    spark = get_spark()
    customers_b = add_ingestion_metadata(ingest_csv(spark, str(DATA / "customers.csv")), "customers.csv")
    accounts_b = add_ingestion_metadata(ingest_csv(spark, str(DATA / "accounts.csv")), "accounts.csv")
    transactions_b = add_ingestion_metadata(ingest_csv(spark, str(DATA / "transactions.csv")), "transactions.csv")

    customers = clean_customers(customers_b)
    accounts = clean_accounts(accounts_b)
    transactions = clean_transactions(transactions_b)

    quality = run_quality_checks(customers, accounts, transactions)
    failed = [name for name, value in quality.items() if value is False or (isinstance(value, dict) and not all(value.values()))]
    if failed:
        raise ValueError(f"Data quality checks failed: {failed}")

    enriched = enrich_transactions(transactions, accounts, customers)
    gold = {
        "customer_360": customer_360(customers, accounts, enriched),
        "monthly_transaction_trends": monthly_transaction_trends(enriched),
        "customer_spending_analysis": customer_spending_analysis(enriched),
        "account_kpis": account_kpis(accounts),
        "category_analysis": category_analysis(enriched),
    }

    for name, df in gold.items():
        path = OUTPUT / name
        df.coalesce(1).write.mode("overwrite").option("header", True).csv(str(path))
        print(f"\n=== {name} ===")
        df.show(20, truncate=False)

    print("\nPipeline completed successfully.")
    spark.stop()


if __name__ == "__main__":
    main()

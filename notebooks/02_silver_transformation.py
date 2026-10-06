from pathlib import Path
from src.utils.spark_session import get_spark
from src.bronze.ingestion import ingest_csv
from src.silver.transformations import clean_customers, clean_accounts, clean_transactions, enrich_transactions

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw"
spark = get_spark("SilverTransformation")

customers = clean_customers(ingest_csv(spark, str(DATA / "customers.csv")))
accounts = clean_accounts(ingest_csv(spark, str(DATA / "accounts.csv")))
transactions = clean_transactions(ingest_csv(spark, str(DATA / "transactions.csv")))
enriched = enrich_transactions(transactions, accounts, customers)

enriched.show(20, truncate=False)
spark.stop()

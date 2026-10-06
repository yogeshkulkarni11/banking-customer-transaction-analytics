from pathlib import Path
from src.utils.spark_session import get_spark
from src.bronze.ingestion import ingest_csv, add_ingestion_metadata

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw"

spark = get_spark("BronzeIngestion")

for name in ["customers", "accounts", "transactions"]:
    df = ingest_csv(spark, str(DATA / f"{name}.csv"))
    bronze = add_ingestion_metadata(df, f"{name}.csv")
    print(f"Bronze: {name}")
    bronze.show(5, truncate=False)

spark.stop()

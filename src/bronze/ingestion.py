from pyspark.sql import DataFrame, SparkSession


def ingest_csv(spark: SparkSession, path: str) -> DataFrame:
    return spark.read.option("header", True).option("inferSchema", True).csv(path)


def add_ingestion_metadata(df: DataFrame, source_file: str) -> DataFrame:
    from pyspark.sql import functions as F
    return df.withColumn("ingestion_timestamp", F.current_timestamp()).withColumn("source_file", F.lit(source_file))

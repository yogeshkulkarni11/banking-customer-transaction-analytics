from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def clean_customers(df: DataFrame) -> DataFrame:
    return (
        df.dropDuplicates(["customer_id"])
        .withColumn("join_date", F.to_date("join_date"))
        .filter(F.col("customer_id").isNotNull())
    )


def clean_accounts(df: DataFrame) -> DataFrame:
    return (
        df.dropDuplicates(["account_id"])
        .withColumn("opening_date", F.to_date("opening_date"))
        .withColumn("balance", F.col("balance").cast("double"))
        .filter(F.col("account_id").isNotNull() & F.col("customer_id").isNotNull())
    )


def clean_transactions(df: DataFrame) -> DataFrame:
    return (
        df.dropDuplicates(["transaction_id"])
        .withColumn("transaction_date", F.to_date("transaction_date"))
        .withColumn("amount", F.col("amount").cast("double"))
        .filter(
            F.col("transaction_id").isNotNull()
            & F.col("account_id").isNotNull()
            & F.col("customer_id").isNotNull()
            & F.col("amount").isNotNull()
            & (F.col("amount") >= 0)
        )
    )


def enrich_transactions(transactions: DataFrame, accounts: DataFrame, customers: DataFrame) -> DataFrame:
    return (
        transactions.filter(F.col("status") == "Success")
        .join(accounts.select("account_id", "account_type", "balance"), "account_id", "left")
        .join(customers.select("customer_id", "customer_name", "city", "customer_segment"), "customer_id", "left")
        .withColumn("transaction_month", F.date_format("transaction_date", "yyyy-MM"))
        .withColumn(
            "signed_amount",
            F.when(F.col("transaction_type") == "Debit", -F.col("amount"))
             .otherwise(F.col("amount"))
        )
    )

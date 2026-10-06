from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def check_not_null(df: DataFrame, columns: list[str]) -> dict:
    return {c: df.filter(F.col(c).isNull()).count() == 0 for c in columns}


def check_unique(df: DataFrame, column: str) -> bool:
    return df.select(column).count() == df.select(column).distinct().count()


def check_non_negative(df: DataFrame, column: str) -> bool:
    return df.filter(F.col(column) < 0).count() == 0


def run_quality_checks(customers: DataFrame, accounts: DataFrame, transactions: DataFrame) -> dict:
    return {
        "customers_required_not_null": check_not_null(customers, ["customer_id", "customer_name"]),
        "customer_id_unique": check_unique(customers, "customer_id"),
        "account_id_unique": check_unique(accounts, "account_id"),
        "transaction_id_unique": check_unique(transactions, "transaction_id"),
        "transaction_amount_non_negative": check_non_negative(transactions, "amount"),
        "transaction_table_not_empty": transactions.limit(1).count() == 1,
    }

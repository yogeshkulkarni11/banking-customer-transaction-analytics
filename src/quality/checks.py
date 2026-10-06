from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def check_not_null(df: DataFrame, columns: list[str]) -> dict:
    return {c: df.filter(F.col(c).isNull()).count() == 0 for c in columns}


def check_unique(df: DataFrame, column: str) -> bool:
    return df.select(column).count() == df.select(column).distinct().count()


def check_non_negative(df: DataFrame, column: str) -> bool:
    return df.filter(F.col(column) < 0).count() == 0


def check_referential_integrity(child: DataFrame, child_column: str, parent: DataFrame, parent_column: str) -> bool:
    parent_keys = parent.select(F.col(parent_column).alias("_parent_key")).distinct()
    orphan_count = (
        child.select(F.col(child_column).alias("_child_key"))
        .join(parent_keys, F.col("_child_key") == F.col("_parent_key"), "left_anti")
        .count()
    )
    return orphan_count == 0


def check_allowed_values(df: DataFrame, column: str, allowed_values: set[str]) -> bool:
    invalid = df.filter(~F.col(column).isin(list(allowed_values))).limit(1).count()
    return invalid == 0


def run_quality_checks(customers: DataFrame, accounts: DataFrame, transactions: DataFrame) -> dict:
    return {
        "customers_required_not_null": check_not_null(customers, ["customer_id", "customer_name"]),
        "accounts_required_not_null": check_not_null(accounts, ["account_id", "customer_id"]),
        "transactions_required_not_null": check_not_null(
            transactions, ["transaction_id", "account_id", "customer_id", "amount"]
        ),
        "customer_id_unique": check_unique(customers, "customer_id"),
        "account_id_unique": check_unique(accounts, "account_id"),
        "transaction_id_unique": check_unique(transactions, "transaction_id"),
        "transaction_amount_non_negative": check_non_negative(transactions, "amount"),
        "account_customer_fk_valid": check_referential_integrity(
            accounts, "customer_id", customers, "customer_id"
        ),
        "transaction_account_fk_valid": check_referential_integrity(
            transactions, "account_id", accounts, "account_id"
        ),
        "transaction_customer_fk_valid": check_referential_integrity(
            transactions, "customer_id", customers, "customer_id"
        ),
        "transaction_status_valid": check_allowed_values(
            transactions, "status", {"Success", "Failed"}
        ),
        "transaction_type_valid": check_allowed_values(
            transactions, "transaction_type", {"Debit", "Credit"}
        ),
        "transaction_table_not_empty": transactions.limit(1).count() == 1,
    }

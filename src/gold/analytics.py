from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def customer_360(customers: DataFrame, accounts: DataFrame, transactions: DataFrame) -> DataFrame:
    tx = transactions.groupBy("customer_id").agg(
        F.count("transaction_id").alias("transaction_count"),
        F.sum(F.when(F.col("transaction_type") == "Debit", F.col("amount")).otherwise(0)).alias("total_debit"),
        F.sum(F.when(F.col("transaction_type") == "Credit", F.col("amount")).otherwise(0)).alias("total_credit"),
        F.sum("signed_amount").alias("net_transaction_value"),
    )
    acct = accounts.groupBy("customer_id").agg(
        F.count("account_id").alias("account_count"),
        F.sum("balance").alias("total_balance"),
    )
    return customers.join(acct, "customer_id", "left").join(tx, "customer_id", "left").fillna(0)


def monthly_transaction_trends(transactions: DataFrame) -> DataFrame:
    monthly = transactions.groupBy("transaction_month", "transaction_type").agg(
        F.count("transaction_id").alias("transaction_count"),
        F.sum("amount").alias("transaction_value"),
        F.avg("amount").alias("average_transaction_value"),
    )
    trend_window = Window.partitionBy("transaction_type").orderBy("transaction_month")
    return (
        monthly
        .withColumn("previous_month_value", F.lag("transaction_value").over(trend_window))
        .withColumn(
            "mom_change_pct",
            F.when(
                F.col("previous_month_value").isNull() | (F.col("previous_month_value") == 0),
                F.lit(None).cast("double"),
            ).otherwise(
                (F.col("transaction_value") - F.col("previous_month_value"))
                / F.col("previous_month_value") * 100
            ),
        )
        .withColumn(
            "running_transaction_value",
            F.sum("transaction_value").over(
                trend_window.rowsBetween(Window.unboundedPreceding, Window.currentRow)
            ),
        )
        .orderBy("transaction_month", "transaction_type")
    )


def customer_spending_analysis(transactions: DataFrame) -> DataFrame:
    debit = transactions.filter(F.col("transaction_type") == "Debit")
    w = Window.orderBy(F.desc("total_spend"))
    return (
        debit.groupBy("customer_id", "customer_name", "customer_segment")
        .agg(
            F.sum("amount").alias("total_spend"),
            F.count("transaction_id").alias("debit_count"),
        )
        .withColumn("spend_rank", F.dense_rank().over(w))
        .orderBy("spend_rank")
    )


def account_kpis(accounts: DataFrame) -> DataFrame:
    return accounts.groupBy("account_type", "status").agg(
        F.count("account_id").alias("account_count"),
        F.sum("balance").alias("total_balance"),
        F.avg("balance").alias("average_balance"),
    )


def category_analysis(transactions: DataFrame) -> DataFrame:
    return (
        transactions.filter(F.col("transaction_type") == "Debit")
        .groupBy("category")
        .agg(
            F.count("transaction_id").alias("transaction_count"),
            F.sum("amount").alias("total_spend"),
            F.avg("amount").alias("average_spend"),
        )
        .orderBy(F.desc("total_spend"))
    )

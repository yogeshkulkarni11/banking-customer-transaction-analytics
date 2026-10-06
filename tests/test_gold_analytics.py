from src.gold.analytics import customer_spending_analysis, monthly_transaction_trends


def test_customer_spending_ranking(spark):
    rows = [
        ("T1", "C1", "Alice", "Premium", "2025-01", "Debit", 500.0, -500.0),
        ("T2", "C1", "Alice", "Premium", "2025-01", "Debit", 300.0, -300.0),
        ("T3", "C2", "Bob", "Standard", "2025-01", "Debit", 1000.0, -1000.0),
    ]
    columns = [
        "transaction_id", "customer_id", "customer_name", "customer_segment",
        "transaction_month", "transaction_type", "amount", "signed_amount",
    ]
    df = spark.createDataFrame(rows, columns)
    result = customer_spending_analysis(df).collect()

    assert result[0]["customer_id"] == "C2"
    assert result[0]["spend_rank"] == 1
    assert result[1]["total_spend"] == 800.0


def test_monthly_trends_running_total_and_mom(spark):
    rows = [
        ("2025-01", "Debit", 100.0),
        ("2025-02", "Debit", 150.0),
    ]
    df = spark.createDataFrame(rows, ["transaction_month", "transaction_type", "amount"])
    df = df.withColumn("transaction_id", df.transaction_month)

    result = monthly_transaction_trends(
        df.select("transaction_id", "transaction_month", "transaction_type", "amount")
    ).collect()

    assert result[0]["running_transaction_value"] == 100.0
    assert result[1]["running_transaction_value"] == 250.0
    assert round(result[1]["mom_change_pct"], 2) == 50.0

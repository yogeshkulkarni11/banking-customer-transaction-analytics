from src.quality.checks import (
    check_allowed_values,
    check_non_negative,
    check_not_null,
    check_referential_integrity,
    check_unique,
)


def test_unique(spark):
    df = spark.createDataFrame([(1,), (2,), (3,)], ["id"])
    assert check_unique(df, "id")


def test_non_negative(spark):
    df = spark.createDataFrame([(10.0,), (0.0,)], ["amount"])
    assert check_non_negative(df, "amount")


def test_not_null(spark):
    df = spark.createDataFrame([(1, "A"), (2, "B")], ["id", "name"])
    assert check_not_null(df, ["id", "name"]) == {"id": True, "name": True}


def test_referential_integrity(spark):
    parent = spark.createDataFrame([("C001",), ("C002",)], ["customer_id"])
    child = spark.createDataFrame([("A001", "C001"), ("A002", "C002")], ["account_id", "customer_id"])
    assert check_referential_integrity(child, "customer_id", parent, "customer_id")


def test_referential_integrity_detects_orphan(spark):
    parent = spark.createDataFrame([("C001",)], ["customer_id"])
    child = spark.createDataFrame([("A001", "C999")], ["account_id", "customer_id"])
    assert not check_referential_integrity(child, "customer_id", parent, "customer_id")


def test_allowed_values(spark):
    df = spark.createDataFrame([("Success",), ("Failed",)], ["status"])
    assert check_allowed_values(df, "status", {"Success", "Failed"})

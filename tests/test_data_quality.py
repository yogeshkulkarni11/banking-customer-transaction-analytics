from src.quality.checks import check_non_negative, check_unique


def test_unique(spark):
    df = spark.createDataFrame([(1,), (2,), (3,)], ["id"])
    assert check_unique(df, "id")


def test_non_negative(spark):
    df = spark.createDataFrame([(10.0,), (0.0,)], ["amount"])
    assert check_non_negative(df, "amount")

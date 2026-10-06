import pytest
from src.utils.spark_session import get_spark


@pytest.fixture(scope="session")
def spark():
    session = get_spark("BankingAnalyticsTests")
    yield session
    session.stop()

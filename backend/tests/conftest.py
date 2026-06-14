import warnings

import pytest  # pyright: ignore[reportMissingImports]

# Suppress DeprecationWarning triggered by third-party libs using
# asyncio.iscoroutinefunction which is deprecated in Python 3.14+.
# This keeps test runs clean while upstream libs are updated.
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    message=r".*asyncio.iscoroutinefunction.*",
)


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "unit: unit tests")
    config.addinivalue_line("markers", "integration: integration tests")
    config.addinivalue_line("markers", "slow: slow running tests")


@pytest.fixture
def test_settings():
    """Provide test configuration settings."""
    return {
        "log_level": "DEBUG",
        "test_mode": True,
    }

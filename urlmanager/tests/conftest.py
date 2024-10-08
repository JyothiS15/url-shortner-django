import pytest


@pytest.fixture
def shortend_url() -> str:
    """
    random string of length 7
    """
    return "DFt3WyE"


@pytest.fixture
def true_existance_status() -> bool:
    """
    default to True
    """
    return True

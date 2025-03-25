"""
Unit test for API.
"""
import pytest
from app import init_app

@pytest.fixture
def initialize_api():
    """
    """
    app = init_app()

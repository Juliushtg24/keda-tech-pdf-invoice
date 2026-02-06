"""
Pytest fixtures and configuration for unit tests.
"""
import pytest
from datetime import date
from fastapi.testclient import TestClient

from app.main import app
from app.models import InvoiceRequest


@pytest.fixture
def test_client():
    """Create a test client for FastAPI application."""
    return TestClient(app)


@pytest.fixture
def sample_invoice_data() -> dict:
    """Sample invoice data as dictionary for API requests."""
    return {
        "customer_name": "Julius Martin",
        "guide_name": "Bali Explorer",
        "date": "2026-04-05",
        "price": 1500000000,
        "currency": "IDR"
    }


@pytest.fixture
def sample_invoice_request() -> InvoiceRequest:
    """Sample InvoiceRequest model instance for PDF generation tests."""
    return InvoiceRequest(
        customer_name="Julius Martin",
        guide_name="Bali Explorer",
        date=date(2026, 4, 5),
        price=1500000000,
        currency="IDR"
    )


@pytest.fixture
def invalid_invoice_data() -> dict:
    """Invalid invoice data for negative test cases."""
    return {
        "customer_name": "",
        "guide_name": "Bali Explorer",
        "date": "invalid-date",
        "price": "not-a-number",
        "currency": "USD"
    }

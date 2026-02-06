"""
Unit tests for Pydantic models.
"""
import pytest
from datetime import date
from pydantic import ValidationError

from app.models import InvoiceRequest


class TestInvoiceRequest:
    """Test cases for InvoiceRequest model."""

    def test_valid_invoice_request(self):
        """Should create InvoiceRequest with valid data."""
        invoice = InvoiceRequest(
            customer_name="Julius Martin",
            guide_name="Bali Explorer",
            date=date(2026, 4, 5),
            price=1500000000,
            currency="IDR"
        )

        assert invoice.customer_name == "Julius Martin"
        assert invoice.guide_name == "Bali Explorer"
        assert invoice.date == date(2026, 4, 5)
        assert invoice.price == 1500000000
        assert invoice.currency == "IDR"

    def test_invoice_request_with_string_date(self):
        """Should parse string date to date object."""
        invoice = InvoiceRequest(
            customer_name="Jane Smith",
            guide_name="Tokyo Guide",
            date="2026-05-10",
            price=200.00,
            currency="JPY"
        )

        assert invoice.date == date(2026, 5, 10)

    def test_invoice_request_with_integer_price(self):
        """Should accept integer price and convert to float."""
        invoice = InvoiceRequest(
            customer_name="Test User",
            guide_name="Test Guide",
            date="2026-01-01",
            price=100,
            currency="EUR"
        )

        assert invoice.price == 100.0

    def test_invoice_request_with_large_price(self):
        """Should handle large price values."""
        invoice = InvoiceRequest(
            customer_name="VIP Customer",
            guide_name="Premium Guide",
            date="2026-12-31",
            price=100000000,
            currency="IDR"
        )

        assert invoice.price == 100000000

    def test_invoice_request_missing_customer_name(self):
        """Should raise ValidationError when customer_name is missing."""
        with pytest.raises(ValidationError):
            InvoiceRequest(
                guide_name="Bali Explorer",
                date="2026-04-05",
                price=1500000000,
                currency="IDR"
            )

    def test_invoice_request_missing_guide_name(self):
        """Should raise ValidationError when guide_name is missing."""
        with pytest.raises(ValidationError):
            InvoiceRequest(
                customer_name="Julius Martin",
                date="2026-04-05",
                price=1500000000,
                currency="IDR"
            )

    def test_invoice_request_invalid_date_format(self):
        """Should raise ValidationError for invalid date format."""
        with pytest.raises(ValidationError):
            InvoiceRequest(
                customer_name="Julius Martin",
                guide_name="Bali Explorer",
                date="05-04-2026",  # Invalid format
                price=1500000000,
                currency="IDR"
            )

    def test_invoice_request_invalid_price_type(self):
        """Should raise ValidationError for non-numeric price."""
        with pytest.raises(ValidationError):
            InvoiceRequest(
                customer_name="Julius Martin",
                guide_name="Bali Explorer",
                date="2026-04-05",
                price="expensive",
                currency="IDR"
            )

    def test_invoice_request_missing_currency(self):
        """Should raise ValidationError when currency is missing."""
        with pytest.raises(ValidationError):
            InvoiceRequest(
                customer_name="Julius Martin",
                guide_name="Bali Explorer",
                date="2026-04-05",
                price=1500000000
            )

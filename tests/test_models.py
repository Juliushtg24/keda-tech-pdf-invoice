"""
Unit tests for Pydantic models.
"""
import pytest
from datetime import date
from pydantic import ValidationError

from app.models import InvoiceRequest, InvoiceItem


class TestInvoiceItem:
    """Test cases for InvoiceItem model."""

    def test_valid_invoice_item(self):
        """Should create InvoiceItem with valid data."""
        item = InvoiceItem(description="Tour Guide Service", quantity=2, price=500.00)

        assert item.description == "Tour Guide Service"
        assert item.quantity == 2
        assert item.price == 500.00

    def test_invoice_item_missing_description(self):
        """Should raise ValidationError when description is missing."""
        with pytest.raises(ValidationError):
            InvoiceItem(quantity=1, price=100.00)


class TestInvoiceRequest:
    """Test cases for InvoiceRequest model."""

    def test_valid_invoice_request(self):
        """Should create InvoiceRequest with valid data."""
        invoice = InvoiceRequest(
            customer_name="Julius Martin",
            guide_name="Bali Explorer",
            date=date(2026, 4, 5),
            items=[
                {"description": "Tour Guide Service", "quantity": 1, "price": 1500000000}
            ],
            currency="IDR"
        )

        assert invoice.customer_name == "Julius Martin"
        assert invoice.guide_name == "Bali Explorer"
        assert invoice.date == date(2026, 4, 5)
        assert len(invoice.items) == 1
        assert invoice.items[0].price == 1500000000
        assert invoice.currency == "IDR"

    def test_invoice_request_with_string_date(self):
        """Should parse string date to date object."""
        invoice = InvoiceRequest(
            customer_name="Jane Smith",
            guide_name="Tokyo Guide",
            date="2026-05-10",
            items=[
                {"description": "City Tour", "quantity": 1, "price": 200.00}
            ],
            currency="JPY"
        )

        assert invoice.date == date(2026, 5, 10)

    def test_invoice_request_subtotal(self):
        """Should calculate subtotal correctly from items."""
        invoice = InvoiceRequest(
            customer_name="Test User",
            guide_name="Test Guide",
            date="2026-01-01",
            items=[
                {"description": "Tour A", "quantity": 2, "price": 100.00},
                {"description": "Tour B", "quantity": 1, "price": 50.00}
            ],
            currency="EUR"
        )

        assert invoice.subtotal == 250.00  # (2*100) + (1*50)

    def test_invoice_request_grand_total_includes_tax(self):
        """Should calculate grand total with 11% tax."""
        invoice = InvoiceRequest(
            customer_name="Test User",
            guide_name="Test Guide",
            date="2026-01-01",
            items=[
                {"description": "Tour", "quantity": 1, "price": 100.00}
            ],
            currency="EUR"
        )

        assert invoice.grandTotal == pytest.approx(111.00, rel=1e-2)

    def test_invoice_request_with_large_price(self):
        """Should handle large price values."""
        invoice = InvoiceRequest(
            customer_name="VIP Customer",
            guide_name="Premium Guide",
            date="2026-12-31",
            items=[
                {"description": "Premium Service", "quantity": 1, "price": 100000000}
            ],
            currency="IDR"
        )

        assert invoice.items[0].price == 100000000

    def test_invoice_request_missing_customer_name(self):
        """Should raise ValidationError when customer_name is missing."""
        with pytest.raises(ValidationError):
            InvoiceRequest(
                guide_name="Bali Explorer",
                date="2026-04-05",
                items=[
                    {"description": "Tour", "quantity": 1, "price": 1500000000}
                ],
                currency="IDR"
            )

    def test_invoice_request_missing_guide_name(self):
        """Should raise ValidationError when guide_name is missing."""
        with pytest.raises(ValidationError):
            InvoiceRequest(
                customer_name="Julius Martin",
                date="2026-04-05",
                items=[
                    {"description": "Tour", "quantity": 1, "price": 1500000000}
                ],
                currency="IDR"
            )

    def test_invoice_request_invalid_date_format(self):
        """Should raise ValidationError for invalid date format."""
        with pytest.raises(ValidationError):
            InvoiceRequest(
                customer_name="Julius Martin",
                guide_name="Bali Explorer",
                date="05-04-2026",  # Invalid format
                items=[
                    {"description": "Tour", "quantity": 1, "price": 1500000000}
                ],
                currency="IDR"
            )

    def test_invoice_request_invalid_items(self):
        """Should raise ValidationError for invalid items."""
        with pytest.raises(ValidationError):
            InvoiceRequest(
                customer_name="Julius Martin",
                guide_name="Bali Explorer",
                date="2026-04-05",
                items="not-a-list",
                currency="IDR"
            )

    def test_invoice_request_missing_currency(self):
        """Should raise ValidationError when currency is missing."""
        with pytest.raises(ValidationError):
            InvoiceRequest(
                customer_name="Julius Martin",
                guide_name="Bali Explorer",
                date="2026-04-05",
                items=[
                    {"description": "Tour", "quantity": 1, "price": 1500000000}
                ]
            )

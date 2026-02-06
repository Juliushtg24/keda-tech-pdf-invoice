"""
Unit tests for PDF generation functionality.
"""
import pytest
from io import BytesIO
from datetime import date

from app.models import InvoiceRequest
from app.pdf import generate_invoice_pdf


class TestGenerateInvoicePdf:
    """Test cases for generate_invoice_pdf function."""

    def test_returns_bytes_buffer(self, sample_invoice_request):
        """Should return a BytesIO buffer."""
        result = generate_invoice_pdf(sample_invoice_request)

        assert isinstance(result, BytesIO)

    def test_buffer_is_not_empty(self, sample_invoice_request):
        """Should generate non-empty PDF content."""
        result = generate_invoice_pdf(sample_invoice_request)
        content = result.read()

        assert len(content) > 0

    def test_buffer_contains_pdf_header(self, sample_invoice_request):
        """Should generate valid PDF with correct header."""
        result = generate_invoice_pdf(sample_invoice_request)
        content = result.read()

        # PDF files start with %PDF
        assert content.startswith(b'%PDF')

    def test_buffer_is_seeked_to_start(self, sample_invoice_request):
        """Should return buffer with position at start."""
        result = generate_invoice_pdf(sample_invoice_request)

        assert result.tell() == 0

    def test_pdf_with_different_currencies(self):
        """Should generate PDF for various currencies."""
        currencies = ["USD", "EUR", "IDR", "JPY", "GBP"]

        for currency in currencies:
            request = InvoiceRequest(
                customer_name="Test User",
                guide_name="Test Guide",
                date=date(2026, 1, 1),
                price=100.00,
                currency=currency
            )

            result = generate_invoice_pdf(request)
            content = result.read()

            assert content.startswith(b'%PDF')
            assert len(content) > 0

    def test_pdf_with_long_customer_name(self):
        """Should handle long customer names."""
        request = InvoiceRequest(
            customer_name="Very Long Customer Name That Might Overflow",
            guide_name="Bali Explorer",
            date=date(2026, 4, 5),
            price=1500000000,
            currency="IDR"
        )

        result = generate_invoice_pdf(request)
        content = result.read()

        assert content.startswith(b'%PDF')

    def test_pdf_with_long_guide_name(self):
        """Should handle long guide names."""
        request = InvoiceRequest(
            customer_name="Julius Martin",
            guide_name="Extremely Long Guide Name For Testing Purposes",
            date=date(2026, 4, 5),
            price=1500000000,
            currency="IDR"
        )

        result = generate_invoice_pdf(request)
        content = result.read()

        assert content.startswith(b'%PDF')

    def test_pdf_with_zero_price(self):
        """Should handle zero price (complimentary service)."""
        request = InvoiceRequest(
            customer_name="Julius Martin",
            guide_name="Bali Explorer",
            date=date(2026, 4, 5),
            price=0.00,
            currency="IDR"
        )

        result = generate_invoice_pdf(request)
        content = result.read()

        assert content.startswith(b'%PDF')

    def test_pdf_with_decimal_price(self):
        """Should handle decimal price values."""
        request = InvoiceRequest(
            customer_name="Julius Martin",
            guide_name="Bali Explorer",
            date=date(2026, 4, 5),
            price=1500000000.50,
            currency="IDR"
        )

        result = generate_invoice_pdf(request)
        content = result.read()

        assert content.startswith(b'%PDF')

    def test_pdf_with_large_price(self):
        """Should handle large price values."""
        request = InvoiceRequest(
            customer_name="Julius Martin",
            guide_name="Bali Explorer",
            date=date(2026, 4, 5),
            price=1500000000,
            currency="IDR"
        )

        result = generate_invoice_pdf(request)
        content = result.read()

        assert content.startswith(b'%PDF')

    def test_multiple_pdf_generations(self, sample_invoice_request):
        """Should generate multiple PDFs independently."""
        result1 = generate_invoice_pdf(sample_invoice_request)
        result2 = generate_invoice_pdf(sample_invoice_request)

        content1 = result1.read()
        content2 = result2.read()

        # Both should be valid PDFs
        assert content1.startswith(b'%PDF')
        assert content2.startswith(b'%PDF')

        # Should be independent buffers
        assert result1 is not result2

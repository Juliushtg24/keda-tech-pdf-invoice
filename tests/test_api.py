"""
Unit tests for API endpoints.
"""
import pytest


class TestHealthCheck:
    """Test cases for health check endpoint."""

    def test_health_check_returns_200(self, test_client):
        """Should return 200 status code."""
        response = test_client.get("/")

        assert response.status_code == 200

    def test_health_check_returns_correct_json(self, test_client):
        """Should return correct status message."""
        response = test_client.get("/")
        data = response.json()

        assert data["status"] == "ok"
        assert data["message"] == "Invoice API is running"


class TestGenerateInvoice:
    """Test cases for /generate-invoice endpoint."""

    def test_generate_invoice_returns_200(self, test_client, sample_invoice_data):
        """Should return 200 status code for valid request."""
        response = test_client.post("/generate-invoice", json=sample_invoice_data)

        assert response.status_code == 200

    def test_generate_invoice_returns_pdf_content_type(self, test_client, sample_invoice_data):
        """Should return PDF content type."""
        response = test_client.post("/generate-invoice", json=sample_invoice_data)

        assert response.headers["content-type"] == "application/pdf"

    def test_generate_invoice_returns_attachment_header(self, test_client, sample_invoice_data):
        """Should include content-disposition header for download."""
        response = test_client.post("/generate-invoice", json=sample_invoice_data)

        assert "attachment" in response.headers["content-disposition"]
        assert "invoice.pdf" in response.headers["content-disposition"]

    def test_generate_invoice_returns_pdf_content(self, test_client, sample_invoice_data):
        """Should return valid PDF content."""
        response = test_client.post("/generate-invoice", json=sample_invoice_data)

        assert response.content.startswith(b'%PDF')

    def test_generate_invoice_missing_customer_name(self, test_client):
        """Should return 422 when customer_name is missing."""
        data = {
            "guide_name": "Bali Explorer",
            "date": "2026-04-05",
            "price": 1500000000,
            "currency": "IDR"
        }

        response = test_client.post("/generate-invoice", json=data)

        assert response.status_code == 422

    def test_generate_invoice_missing_guide_name(self, test_client):
        """Should return 422 when guide_name is missing."""
        data = {
            "customer_name": "Julius Martin",
            "date": "2026-04-05",
            "price": 1500000000,
            "currency": "IDR"
        }

        response = test_client.post("/generate-invoice", json=data)

        assert response.status_code == 422

    def test_generate_invoice_invalid_date(self, test_client):
        """Should return 422 for invalid date format."""
        data = {
            "customer_name": "Julius Martin",
            "guide_name": "Bali Explorer",
            "date": "invalid-date",
            "price": 1500000000,
            "currency": "IDR"
        }

        response = test_client.post("/generate-invoice", json=data)

        assert response.status_code == 422

    def test_generate_invoice_invalid_price(self, test_client):
        """Should return 422 for non-numeric price."""
        data = {
            "customer_name": "Julius Martin",
            "guide_name": "Bali Explorer",
            "date": "2026-04-05",
            "price": "expensive",
            "currency": "IDR"
        }

        response = test_client.post("/generate-invoice", json=data)

        assert response.status_code == 422

    def test_generate_invoice_empty_body(self, test_client):
        """Should return 422 for empty request body."""
        response = test_client.post("/generate-invoice", json={})

        assert response.status_code == 422

    def test_generate_invoice_get_method_not_allowed(self, test_client):
        """Should return 405 for GET method."""
        response = test_client.get("/generate-invoice")

        assert response.status_code == 405


class TestPreviewInvoice:
    """Test cases for /preview-invoice endpoint."""

    def test_preview_invoice_returns_200(self, test_client, sample_invoice_data):
        """Should return 200 status code for valid request."""
        response = test_client.post("/preview-invoice", json=sample_invoice_data)

        assert response.status_code == 200

    def test_preview_invoice_returns_pdf_content_type(self, test_client, sample_invoice_data):
        """Should return PDF content type."""
        response = test_client.post("/preview-invoice", json=sample_invoice_data)

        assert response.headers["content-type"] == "application/pdf"

    def test_preview_invoice_returns_inline_header(self, test_client, sample_invoice_data):
        """Should include content-disposition header for inline viewing."""
        response = test_client.post("/preview-invoice", json=sample_invoice_data)

        assert "inline" in response.headers["content-disposition"]
        assert "invoice.pdf" in response.headers["content-disposition"]

    def test_preview_invoice_returns_pdf_content(self, test_client, sample_invoice_data):
        """Should return valid PDF content."""
        response = test_client.post("/preview-invoice", json=sample_invoice_data)

        assert response.content.startswith(b'%PDF')

    def test_preview_invoice_missing_fields(self, test_client):
        """Should return 422 when required fields are missing."""
        data = {"customer_name": "Julius Martin"}

        response = test_client.post("/preview-invoice", json=data)

        assert response.status_code == 422

    def test_preview_invoice_get_method_not_allowed(self, test_client):
        """Should return 405 for GET method."""
        response = test_client.get("/preview-invoice")

        assert response.status_code == 405


class TestNonExistentEndpoint:
    """Test cases for non-existent endpoints."""

    def test_non_existent_endpoint_returns_404(self, test_client):
        """Should return 404 for non-existent endpoint."""
        response = test_client.get("/non-existent")

        assert response.status_code == 404

    def test_non_existent_post_endpoint_returns_404(self, test_client):
        """Should return 404 for non-existent POST endpoint."""
        response = test_client.post("/create-something", json={})

        assert response.status_code == 404

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

from io import BytesIO

# Color Theme - White and Green
PRIMARY_GREEN = HexColor("#2E7D32")
LIGHT_GREEN = HexColor("#E8F5E9")
DARK_TEXT = HexColor("#333333")
GRAY_TEXT = HexColor("#666666")
WHITE = HexColor("#FFFFFF")
BORDER_GRAY = HexColor("#E0E0E0")


def generate_invoice_pdf(data):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin = 50
    pdf.setTitle("Invoice - KEDA TECH")

    # ==================== HEADER ====================
    # Top green stripe
    pdf.setFillColor(PRIMARY_GREEN)
    pdf.rect(0, height - 8, width, 8, fill=1, stroke=0)

    # Company Name
    pdf.setFillColor(PRIMARY_GREEN)
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawString(margin, height - 60, "KEDA TECH")

    # INVOICE title - right aligned
    pdf.setFont("Helvetica-Bold", 32)
    pdf.drawRightString(width - margin, height - 60, "INVOICE")

    # Divider line
    pdf.setStrokeColor(BORDER_GRAY)
    pdf.setLineWidth(1)
    pdf.line(margin, height - 80, width - margin, height - 80)

    # ==================== INVOICE INFO ====================
    y = height - 120

    # Left column - Invoice details
    pdf.setFillColor(GRAY_TEXT)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(margin, y, "Invoice Number")
    pdf.drawString(margin, y - 40, "Invoice Date")

    pdf.setFillColor(DARK_TEXT)
    pdf.setFont("Helvetica-Bold", 11)
    invoice_no = f"INV-{str(data.date).replace('-', '')[:8]}"
    pdf.drawString(margin, y - 15, invoice_no)
    pdf.drawString(margin, y - 55, str(data.date))

    # Right column - Bill To
    right_col = width - margin - 180
    pdf.setFillColor(GRAY_TEXT)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(right_col, y, "Bill To")

    pdf.setFillColor(DARK_TEXT)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(right_col, y - 15, data.customer_name)

    # ==================== SERVICE TABLE ====================
    table_top = height - 220
    table_width = width - (2 * margin)
    row_height = 30

    # Table header background
    pdf.setFillColor(PRIMARY_GREEN)
    pdf.rect(margin, table_top - row_height, table_width, row_height, fill=1, stroke=0)

    # Table header text
    pdf.setFillColor(WHITE)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(margin + 15, table_top - 20, "DESCRIPTION")
    pdf.drawString(margin + 220, table_top - 20, "GUIDE")
    pdf.drawString(margin + 340, table_top - 20, "QTY")
    pdf.drawRightString(width - margin - 15, table_top - 20, "AMOUNT")

    # Table rows - one per item
    row_y = table_top - row_height
    for index, item in enumerate(data.items):
        current_y = row_y - (row_height * index)

        # Alternating row background
        if index % 2 == 0:
            pdf.setFillColor(LIGHT_GREEN)
        else:
            pdf.setFillColor(WHITE)
        pdf.rect(margin, current_y - row_height, table_width, row_height, fill=1, stroke=0)

        # Row text
        text_y = current_y - 20
        pdf.setFillColor(DARK_TEXT)
        pdf.setFont("Helvetica", 10)
        pdf.drawString(margin + 15, text_y, item.description)
        pdf.drawString(margin + 220, text_y, data.guide_name)
        pdf.drawString(margin + 340, text_y, str(item.quantity))
        pdf.setFont("Helvetica-Bold", 10)
        line_total = item.quantity * item.price
        pdf.drawRightString(width - margin - 15, text_y, f"{data.currency} {line_total:,.2f}")

    # Table border around header + all rows
    total_rows = len(data.items)
    table_total_height = row_height * (1 + total_rows)
    pdf.setStrokeColor(BORDER_GRAY)
    pdf.setLineWidth(1)
    pdf.rect(margin, table_top - table_total_height, table_width, table_total_height, fill=0, stroke=1)

    # Horizontal line under header
    pdf.line(margin, table_top - row_height, margin + table_width, table_top - row_height)

    # ==================== TOTALS SECTION ====================
    totals_y = table_top - table_total_height - 25
    total_box_width = 240
    total_box_x = width - margin - total_box_width

    # Subtotal
    pdf.setFillColor(DARK_TEXT)
    pdf.setFont("Helvetica", 11)
    pdf.drawString(total_box_x, totals_y, "Subtotal")
    pdf.drawRightString(width - margin - 15, totals_y, f"{data.currency} {data.subtotal:,.2f}")

    # Tax (11%)
    totals_y -= 22
    pdf.drawString(total_box_x, totals_y, "Tax (11%)")
    tax_amount = data.grandTotal - data.subtotal
    pdf.drawRightString(width - margin - 15, totals_y, f"{data.currency} {tax_amount:,.2f}")

    # Divider line
    totals_y -= 12
    pdf.setStrokeColor(BORDER_GRAY)
    pdf.line(total_box_x, totals_y, width - margin, totals_y)

    # Grand Total box
    totals_y -= 30
    pdf.setFillColor(PRIMARY_GREEN)
    pdf.rect(total_box_x, totals_y - 5, total_box_width, 30, fill=1, stroke=0)

    pdf.setFillColor(WHITE)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(total_box_x + 15, totals_y + 3, "GRAND TOTAL")
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawRightString(width - margin - 15, totals_y + 3, f"{data.currency} {data.grandTotal:,.2f}")

    # ==================== PAYMENT INFO ====================
    info_y = totals_y - 50
    pdf.setFillColor(DARK_TEXT)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(margin, info_y, "Payment Information")

    pdf.setFont("Helvetica", 9)
    pdf.setFillColor(GRAY_TEXT)
    pdf.drawString(margin, info_y - 18, "Please make payment within 30 days of the invoice date.")
    pdf.drawString(margin, info_y - 32, "For questions regarding this invoice, contact us at support@kedatech.com")

    # ==================== FOOTER ====================
    # Bottom green stripe
    pdf.setFillColor(PRIMARY_GREEN)
    pdf.rect(0, 0, width, 50, fill=1, stroke=0)

    # Thank you message
    pdf.setFillColor(WHITE)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawCentredString(width / 2, 28, "Thank you for your business!")
    pdf.setFont("Helvetica", 8)
    pdf.drawCentredString(width / 2, 14, "www.kedatech.com | support@kedatech.com")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer
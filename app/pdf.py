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
    row_height = 40
    
    # Table header background
    pdf.setFillColor(PRIMARY_GREEN)
    pdf.rect(margin, table_top - row_height, table_width, row_height, fill=1, stroke=0)
    
    # Table header text
    pdf.setFillColor(WHITE)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(margin + 15, table_top - 25, "DESCRIPTION")
    pdf.drawString(margin + 250, table_top - 25, "GUIDE")
    pdf.drawRightString(width - margin - 15, table_top - 25, "AMOUNT")
    
    # Table row background
    row_y = table_top - row_height
    pdf.setFillColor(LIGHT_GREEN)
    pdf.rect(margin, row_y - row_height, table_width, row_height, fill=1, stroke=0)
    
    # Table row text
    pdf.setFillColor(DARK_TEXT)
    pdf.setFont("Helvetica", 11)
    pdf.drawString(margin + 15, row_y - 25, "Tour Guide Service")
    pdf.drawString(margin + 250, row_y - 25, data.guide_name)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawRightString(width - margin - 15, row_y - 25, f"{data.currency} {data.price}")
    
    # Table border
    pdf.setStrokeColor(DARK_TEXT)
    pdf.setLineWidth(1)
    pdf.rect(margin, row_y - row_height, table_width, row_height * 2, fill=0, stroke=1)
    
    # ==================== TOTAL SECTION ====================
    total_y = row_y - row_height - 50
    
    # Total box
    total_box_width = 200
    total_box_x = width - margin - total_box_width
    
    pdf.setFillColor(WHITE)
    pdf.setStrokeColor(PRIMARY_GREEN)
    pdf.setLineWidth(1)
    pdf.rect(total_box_x, total_y - 50, total_box_width, 50, fill=1, stroke=1)
    
    pdf.setFillColor(DARK_TEXT)
    pdf.setFont("Helvetica", 11)
    pdf.drawString(total_box_x + 15, total_y - 20, "TOTAL")
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawRightString(width - margin - 15, total_y - 35, f"{data.currency} {data.price}")
    
    # ==================== FOOTER ====================
    # Bottom green stripe
    pdf.setFillColor(PRIMARY_GREEN)
    pdf.rect(0, 0, width, 50, fill=1, stroke=0)
    
    # Thank you message
    pdf.setFillColor(WHITE)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawCentredString(width / 2, 25, "Thank you for your business!")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer
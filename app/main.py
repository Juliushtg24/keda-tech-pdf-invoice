from fastapi import  FastAPI
from fastapi.responses import StreamingResponse
from mangum import Mangum


from app.models import InvoiceRequest
from app.pdf import generate_invoice_pdf




app = FastAPI()


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Invoice API is running"}


@app.post("/generate-invoice")
def genereate_invoice(request: InvoiceRequest):
    pdf_buffer = generate_invoice_pdf(request)
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=invoice.pdf"})


@app.post("/preview-invoice")
def preview_invoice(request: InvoiceRequest):
    pdf_buffer = generate_invoice_pdf(request)
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=invoice.pdf"})

handler = Mangum(app)

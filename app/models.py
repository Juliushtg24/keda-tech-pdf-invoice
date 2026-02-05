from pydantic import BaseModel
from datetime import date


class InvoiceRequest(BaseModel):
    customer_name: str
    guide_name: str
    date: date
    price: float
    currency: str
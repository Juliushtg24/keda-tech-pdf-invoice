from pydantic import BaseModel, EmailStr, Field
from datetime import date


class InvoiceItem(BaseModel):
    description: str
    quantity: int
    price: float = Field(..., gt=0, description="Price must be greater than zero")


class InvoiceRequest(BaseModel):
    customer_name: str
    customer_email: EmailStr | None = Field(default=None, description="Optional email for sending the invoice") 
    guide_name: str
    date: date
    items: list[InvoiceItem]
    currency: str

    @property
    def subtotal(self) -> float:
        return sum(item.quantity * item.price for item in self.items)
    
    @property
    def grand_total(self) -> float:
        return self.subtotal * (1 + 0.11)  # Assuming 11% tax
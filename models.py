from sqlmodel import Field, SQLModel
from typing import Optional
from decimal import Decimal




class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_name: str
    quantity: int = 0
    price: Decimal = Field(max_digits=10, decimal_places= 2)
    
class ItemUpdate(SQLModel):
    product_name: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[Decimal] = None

class ItemCreate(SQLModel):
    product_name: str
    quantity: int
    price: Decimal

class ItemRead(SQLModel):
    product_name: str
    quantity: int
    price: Decimal

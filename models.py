from pydantic import BaseModel

class CartItem(BaseModel):
    id: int
    name: str
    quantity: int

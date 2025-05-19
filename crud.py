from database import cart
from models import CartItem

def get_all_items():
    return cart

def get_item(item_id: int):
    return next((item for item in cart if item.id == item_id), None)

def add_item(item: CartItem):
    cart.append(item)
    return item

def update_item(item_id: int, updated_item: CartItem):
    for index, item in enumerate(cart):
        if item.id == item_id:
            cart[index] = updated_item
            return updated_item
    return None

def delete_item(item_id: int):
    global cart
    cart = [item for item in cart if item.id != item_id]
    return {"message": "Deleted"}

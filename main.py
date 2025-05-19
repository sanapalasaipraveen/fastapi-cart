from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL connection URL
DATABASE_URL = "mysql+pymysql://root@localhost:3306/cartdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    quantity = Column(Integer)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    id: int
    name: str
    quantity: int

@app.get("/cart")
def read_cart():
    session = SessionLocal()
    items = session.query(CartItem).all()
    session.close()
    return items

@app.post("/cart")
def add_item(item: Item):
    session = SessionLocal()
    db_item = CartItem(**item.dict())
    session.add(db_item)
    session.commit()
    session.close()
    return {"message": "Item added"}

@app.get("/cart/{item_id}")
def get_item(item_id: int):
    session = SessionLocal()
    item = session.query(CartItem).filter(CartItem.id == item_id).first()
    session.close()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/cart/{item_id}")
def update_item(item_id: int, item: Item):
    session = SessionLocal()
    db_item = session.query(CartItem).filter(CartItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.name = item.name
    db_item.quantity = item.quantity
    session.commit()
    session.close()
    return {"message": "Item updated"}

@app.delete("/cart/{item_id}")
def delete_item(item_id: int):
    session = SessionLocal()
    db_item = session.query(CartItem).filter(CartItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(db_item)
    session.commit()
    session.close()
    return {"message": "Item deleted"}

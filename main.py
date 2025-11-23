from fastapi import Depends, FastAPI, HTTPException
from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated
from decimal import Decimal


from models import Item, ItemUpdate, ItemCreate, ItemRead
from database import create_db_and_tables, SessionDep

app = FastAPI()



@app.post("/items")
def create_item(item: ItemCreate, session: SessionDep):
        db_item = Item(**item.model_dump())

        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item

@app.get("/items/", response_model=list[ItemRead])
def read_items(session: SessionDep, offset: int = 0):
     items = session.exec(select(Item).offset(offset)).all()
     return items 


@app.get("/items/total-value")
def get_total_value(session:SessionDep):
        items = session.exec(select(Item)).all()
        total = sum(item.price * item.quantity for item in items)
        return {"total_value": str(total)}

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, session: SessionDep):
    item = session.get(Item, item_id)
    if not item:
         raise HTTPException(status_code=404, detail="Item not found")
    return item
     

@app.patch("/items/{item_id}")
def update_item(item_id: int, item: ItemUpdate, session: SessionDep):    
            db_item = session.get(Item, item_id)
            if not db_item:
                raise HTTPException(status_code=404, detail="Item not found")
            item_data = item.model_dump(exclude_unset=True)
            db_item.sqlmodel_update(item_data)
            session.add(db_item)
            session.commit()
            session.refresh(db_item)
            return db_item


@app.delete("/items/{item_id}")
def delete_item(item_id: int, session:SessionDep):
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(db_item)
    session.commit()
    return {"ok": True}   


     

@app.on_event("startup")
def on_startup():
    create_db_and_tables()




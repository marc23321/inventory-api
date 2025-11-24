from sqlmodel import Session, SQLModel, create_engine
from typing import Annotated
from fastapi import Depends
from dotenv import load_dotenv
from models import Item
import os

#Load .env file
load_dotenv()

# Read DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)
connect_args = {}

#Create engine using URL
engine = create_engine(DATABASE_URL, echo=True)

#Create DB Tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
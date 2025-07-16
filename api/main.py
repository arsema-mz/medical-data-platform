from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
from .database import SessionLocal
from . import crud, schemas

app = FastAPI(title="Medical Data Analytical API")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/reports/top-products", response_model=List[schemas.TopProductSchema])
def read_top_products(limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_top_products(db, limit)

@app.get("/api/channels/{channel}/activity", response_model=List[schemas.ChannelActivitySchema])
def read_channel_activity(channel: str, db: Session = Depends(get_db)):
    return crud.get_channel_activity(db, channel)

@app.get("/api/search/messages", response_model=List[schemas.MessageSchema])
def search_messages(query: str, db: Session = Depends(get_db)):
    return crud.search_messages(db, query)

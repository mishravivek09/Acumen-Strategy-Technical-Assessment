from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import ProgrammingError
from database import engine, get_db
from models.customer import Customer
from services.ingestion import run_ingestion

app = FastAPI()

@app.post("/api/ingest")
def ingest_data():
    try:
        result = run_ingestion()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customers")
def get_customers(page: int = Query(1, ge=1), limit: int = Query(10, ge=1), db: Session = Depends(get_db)):
    skip = (page - 1) * limit
    try:
        customers = db.query(Customer).offset(skip).limit(limit).all()
        total = db.query(Customer).count()
        return {
            "data": customers,
            "total": total,
            "page": page,
            "limit": limit
        }
    except ProgrammingError:
        return {"data": [], "total": 0, "page": page, "limit": limit}

@app.get("/api/customers/{id}")
def get_customer(id: str, db: Session = Depends(get_db)):
    try:
        customer = db.query(Customer).filter(Customer.customer_id == id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer
    except ProgrammingError:
        raise HTTPException(status_code=404, detail="Customer not found")
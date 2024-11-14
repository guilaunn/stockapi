from sqlalchemy.orm import Session
from app.models import Stock

def get_stock(db: Session, company_code: str):
    return db.query(Stock).filter(Stock.company_code == company_code).first()

def create_stock(db: Session, stock_data: dict):
    stock = Stock(**stock_data)
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock

def update_stock_amount(db: Session, company_code: str, amount: int):
    stock = get_stock(db, company_code)
    if stock:
        stock.purchased_amount += amount
        db.commit()
        db.refresh(stock)
    return stock

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.models import Base
from app.schemas import StockUpdate
from app.crud import get_stock, create_stock, update_stock_amount
from app.utils import fetch_stock_data
from app.cache import get_cached_data, cache_data  # Import cache functions
from app.scraping import scrape_marketwatch

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Welcome to the Stock Data API!"}

@app.get("/stock/{stock_symbol}")
def get_stock_data(stock_symbol: str, db: Session = Depends(get_db)):
    cached_data = get_cached_data(stock_symbol)
    if cached_data:
        return cached_data

    try:
        stock_data = fetch_stock_data(stock_symbol, "2023-04-20")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    try:
        performance_data, competitors = scrape_marketwatch(stock_symbol)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to scrape MarketWatch: {str(e)}")

    stock_data_combined = {
        "status": "active",
        "purchased_amount": 0,
        "purchased_status": "not purchased",
        "request_data": "2023-04-20",
        "company_code": stock_symbol,
        "company_name": stock_data.get("company_name", "N/A"),
        "open": stock_data.get("open", 0.0),
        "high": stock_data.get("high", 0.0),
        "low": stock_data.get("low", 0.0),
        "close": stock_data.get("close", 0.0),
        "performance_data": performance_data,
        "competitors": competitors
    }

    cache_data(stock_symbol, stock_data_combined)  # Cache the combined data
    stock = get_stock(db, stock_symbol)
    if not stock:
        create_stock(db, stock_data_combined)

    return stock_data_combined

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.models import Base
from app.schemas import StockUpdate
from app.crud import get_stock, create_stock, update_stock_amount
from app.utils import fetch_stock_data
from app.cache import get_cached_data
from app.scraping import scrape_marketwatch

app = FastAPI()

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Welcome to the Stock Data API!"}

@app.get("/stock/{stock_symbol}")
def get_stock_data(stock_symbol: str, db: Session = Depends(get_db)):
    # Check if the data is already in cache
    cached_data = get_cached_data(stock_symbol)
    if cached_data:
        return cached_data

    # Fetch stock data from Polygon.io
    try:
        stock_data = fetch_stock_data(stock_symbol, "2023-04-20")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Scrape additional data from MarketWatch
    try:
        performance_data, competitors = scrape_marketwatch(stock_symbol)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to scrape MarketWatch: {str(e)}")

    # Combine all stock data
    stock_data_combined = {
        "status": "active",  # Example status, update logic as needed
        "purchased_amount": 0,  # Default amount for a new stock entry
        "purchased_status": "not purchased",  # Example status
        "request_data": "2023-04-20",  # Example request date
        "company_code": stock_symbol,
        "company_name": stock_data.get("company_name", "N/A"),
        "open": stock_data.get("open", 0.0),
        "high": stock_data.get("high", 0.0),
        "low": stock_data.get("low", 0.0),
        "close": stock_data.get("close", 0.0),
        "performance_data": performance_data,
        "competitors": competitors
    }

    # Save or update stock data in the database
    stock = get_stock(db, stock_symbol)
    if not stock:
        create_stock(db, stock_data_combined)
    
    return stock_data_combined

@app.post("/stock/{stock_symbol}")
def update_stock(stock_symbol: str, update: StockUpdate, db: Session = Depends(get_db)):
    # Update the purchased amount for the stock
    stock = update_stock_amount(db, stock_symbol, update.amount)
    if stock:
        return {"message": f"{update.amount} units of stock {stock_symbol} were added to your stock record."}
    else:
        raise HTTPException(status_code=404, detail="Stock not found.")

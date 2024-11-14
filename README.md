# Stock Data API
This project is a RESTful API built in Python using FastAPI that retrieves and manages stock data from an external financial API (Polygon.io) and scrapes performance and competitors' information from the MarketWatch website. The API supports fetching and updating stock information and includes features like caching, logging, and data persistence with PostgreSQL.

Features
Retrieve Stock Data: Fetches data from Polygon.io and scrapes additional details from MarketWatch.
Update Purchased Amount: Allows updating the purchased amount for a stock.
Caching: Implements a simple in-memory caching mechanism to optimize data fetching.
Database Persistence: Uses PostgreSQL to store stock and purchase information.
Docker Support: Includes a Dockerfile to run the application in a containerized environment.
Logging: Provides logs for debugging and tracking API activity.
Requirements
Python 3.10 or above
PostgreSQL
Docker (optional, for containerization)
Setup Instructions
1. Clone the Repository
```
git clone https://github.com/guilaunn/stockapi.git
cd stock-data-api
```
2. Create and Activate a Virtual Environment
```
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate      # On Windows
```
3. Install Dependencies
```
pip install -r requirements.txt
```
4. Set Up the Database
Make sure you have PostgreSQL installed and running.
Update the DATABASE_URL in app/database.py to match your PostgreSQL configuration.
Run the following script to create the tables:
```
python setup_database.py
```
6. Set Up Environment Variables
Create a .env file in the root directory and add your environment variables:
```
POLYGON_API_KEY=your_polygon_api_key
DATABASE_URL=postgresql://user:password@localhost:5432/yourdatabase
```
6. Run the API
```
uvicorn main:app --reload
```
The API will be available at http://localhost:8000.

7. Run in Docker (Optional)
To run the application in a Docker container:
```
docker build -t stock-data-api .
docker run -p 8000:8000 stock-data-api
```
Endpoints
[GET] /stock/{stock_symbol}
Fetches stock data for the given symbol.
Returns a JSON object containing all fields of the Stock model.
[POST] /stock/{stock_symbol}
Updates the purchased amount for the stock.
Request body: { "amount": Integer }
Example: { "amount": 5 }
Example Usage
Fetch Stock Data
```
curl --request GET http://localhost:8000/stock/AAPL
```
Update Purchased Amount
```
curl --request POST \
  --url http://localhost:8000/stock/AAPL \
  --header 'Content-Type: application/json' \
  --data '{"amount": 5}'
```
Technical Overview
Framework: FastAPI for building the API.
Database: PostgreSQL for data persistence.
Caching: Simple in-memory caching to reduce API requests.
Scraping: BeautifulSoup for scraping data from MarketWatch.
External API: Polygon.io for stock data.
Containerization: Docker for running the API in a containerized environment.

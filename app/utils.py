import requests

def fetch_stock_data(symbol: str, date: str):
    api_key = "your_polygon_api_key"
    url = f"https://api.polygon.io/v1/open-close/{symbol}/{date}?apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch stock data")

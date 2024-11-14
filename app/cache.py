import time

# Simple in-memory cache dictionary
cache = {}

def get_cached_data(stock_symbol):
    current_time = time.time()
    cached_entry = cache.get(stock_symbol)

    if cached_entry:
        # Check if the cached data is still valid (e.g., cache for 10 minutes)
        if current_time - cached_entry['timestamp'] < 600:
            return cached_entry['data']
    return None

def cache_data(stock_symbol, data):
    cache[stock_symbol] = {
        'data': data,
        'timestamp': time.time()
    }

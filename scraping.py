import requests
from bs4 import BeautifulSoup

def scrape_marketwatch(stock_symbol):
    url = f"https://www.marketwatch.com/investing/stock/{stock_symbol}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Failed to fetch data from MarketWatch.")

    soup = BeautifulSoup(response.content, "html.parser")

    # Example scraping logic for performance data
    performance_data = {
        "five_days": _extract_float(soup, '...selector_for_five_days...'),
        "one_month": _extract_float(soup, '...selector_for_one_month...'),
        "three_months": _extract_float(soup, '...selector_for_three_months...'),
        "year_to_date": _extract_float(soup, '...selector_for_year_to_date...'),
        "one_year": _extract_float(soup, '...selector_for_one_year...')
    }

    # Example scraping logic for competitors
    competitors = []
    competitors_section = soup.select("...selector_for_competitors...")

    for competitor in competitors_section:
        name = competitor.select_one("...selector_for_name...").text.strip()
        market_cap = competitor.select_one("...selector_for_market_cap...").text.strip()
        currency = "USD"  # Assuming USD as the currency, adjust if needed
        value = _parse_market_cap(market_cap)
        competitors.append({
            "name": name,
            "market_cap": {"currency": currency, "value": value}
        })

    return performance_data, competitors

def _extract_float(soup, selector):
    """Utility function to extract and convert a float value from a given selector."""
    element = soup.select_one(selector)
    if element:
        try:
            return float(element.text.strip().replace(",", "").replace("%", ""))
        except ValueError:
            return 0.0
    return 0.0

def _parse_market_cap(market_cap_str):
    """Parses the market capitalization string and returns the value as a float."""
    try:
        if "B" in market_cap_str:
            return float(market_cap_str.replace("B", "").replace(",", "").strip()) * 1e9
        elif "M" in market_cap_str:
            return float(market_cap_str.replace("M", "").replace(",", "").strip()) * 1e6
        else:
            return float(market_cap_str.replace(",", "").strip())
    except ValueError:
        return 0.0

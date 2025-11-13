from bs4 import BeautifulSoup
import requests


def scrape_stock_data(symbol, exchange):
    if exchange == "NASDAQ":
        url = f"http://finance.yahoo.com/quote/{symbol}"
    elif exchange == "NSE":
        symbol = symbol + ".NS"
        url = f"http://finance.yahoo.com/quote/{symbol}?p={symbol}&.tsrc=fin-srch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    current_price = soup.find("fin-streamer", {"data-symbol": {symbol}}).text
    previous_close = soup.find("td", {"data-test": "PREV_CLOSE-value"}).text

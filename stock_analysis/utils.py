import yfinance as yf


def scrape_stock_data(symbol, exchange):
    """
    Fetch comprehensive stock data using yfinance
    Returns a dictionary with all required fields or error
    """
    try:
        # Add exchange suffix for NSE
        if exchange == "NSE":
            ticker_symbol = f"{symbol}.NS"
        elif exchange == "NASDAQ":
            ticker_symbol = symbol
        else:
            return {"error": f"Unsupported exchange: {exchange}"}

        # Fetch stock data
        stock = yf.Ticker(ticker_symbol)
        info = stock.info

        # Get current price
        current_price = info.get("currentPrice") or info.get("regularMarketPrice")

        # If current price not available, get from recent history
        if not current_price:
            hist = stock.history(period="1d")
            if not hist.empty:
                current_price = hist["Close"].iloc[-1]

        # Get previous close
        previous_close = info.get("previousClose") or info.get(
            "regularMarketPreviousClose"
        )

        # Calculate price change and percentage change
        price_changed = None
        percentage_changed = None
        if current_price and previous_close:
            price_changed = current_price - previous_close
            percentage_changed = (price_changed / previous_close) * 100

        # Get 52-week high and low
        week_52_high = info.get("fiftyTwoWeekHigh")
        week_52_low = info.get("fiftyTwoWeekLow")

        # Get market cap
        market_cap = info.get("marketCap")

        # Get P/E ratio
        pe_ratio = info.get("trailingPE") or info.get("forwardPE")

        # Get dividend yield
        dividend_yield = info.get("dividendYield")
        # Convert to percentage if exists
        if dividend_yield:
            dividend_yield = dividend_yield * 100

        # Format values for storage
        return {
            "symbol": ticker_symbol,
            "current_price": f"{current_price:.2f}" if current_price else None,
            "price_changed": f"{price_changed:+.2f}"
            if price_changed
            else None,  # +/- sign
            "percentage_changed": f"{percentage_changed:+.2f}%"
            if percentage_changed
            else None,
            "previous_close": f"{previous_close:.2f}" if previous_close else None,
            "week_52_high": f"{week_52_high:.2f}" if week_52_high else None,
            "week_52_low": f"{week_52_low:.2f}" if week_52_low else None,
            "market_cap": format_market_cap(market_cap) if market_cap else None,
            "pe_ratio": f"{pe_ratio:.2f}" if pe_ratio else None,
            "dividend_yield": f"{dividend_yield:.2f}%" if dividend_yield else None,
        }

    except Exception as e:
        return {"error": f"Failed to fetch data for {symbol}: {str(e)}"}


def format_market_cap(value):
    """
    Format large numbers into readable format (e.g., 1.5T, 250B, 10M)
    """
    if value >= 1_000_000_000_000:  # Trillion
        return f"{value / 1_000_000_000_000:.2f}T"
    elif value >= 1_000_000_000:  # Billion
        return f"{value / 1_000_000_000:.2f}B"
    elif value >= 1_000_000:  # Million
        return f"{value / 1_000_000:.2f}M"
    else:
        return f"{value:,.0f}"

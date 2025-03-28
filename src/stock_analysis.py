import yfinance as yf

def get_stock_price(ticker):
    """Fetches the current stock price using Yahoo Finance."""
    try:
        stock = yf.Ticker(ticker)
        price = stock.info.get("currentPrice", "Price data not available")
        return f"The current price of {ticker} stock is ${price}"
    except Exception as e:
        return f"Error fetching stock price: {str(e)}"

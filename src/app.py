import os
from stock_analysis import get_stock_price
from news_scraper import get_recent_stock_news

# Set API Key
os.environ["OPENAI_API_KEY"] = "your_api_key"

ticker = input("Enter stock ticker (e.g., AAPL for Apple): ").strip().upper()
print(get_stock_price(ticker))
print(get_recent_stock_news(ticker))

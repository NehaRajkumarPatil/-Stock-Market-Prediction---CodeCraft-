from newspaper import Article
import requests

def get_recent_stock_news(ticker):
    """Fetch recent news for a stock."""
    url = f"https://news.google.com/search?q={ticker}+stock&hl=en-US&gl=US&ceid=US:en"
    try:
        article = Article(url)
        article.download()
        article.parse()
        return f"News Title: {article.title}\nSummary: {article.text[:300]}..."
    except Exception as e:
        return f"Error fetching news: {str(e)}"

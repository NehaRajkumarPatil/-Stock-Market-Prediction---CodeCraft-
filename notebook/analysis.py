# Install necessary dependencies
!pip install --upgrade langchain
!pip install duckduckgo-search openai yfinance newspaper3k typeguard

import os
import openai
import yfinance as yf
from newspaper import Article
from langchain.agents import initialize_agent
from langchain.tools import Tool
from langchain.llms import OpenAI
from langchain.tools import DuckDuckGoSearchRun

# Set your OpenAI API Key
API_KEY = "your_openai_api_key_here"
os.environ["OPENAI_API_KEY"] = API_KEY

# Function to fetch stock price
def get_stock_price(ticker):
    """
    Get the current stock price for a given ticker.

    Args:
        ticker: The stock ticker symbol.

    Returns:
        The current stock price.
    """
    try:
        stock = yf.Ticker(ticker)
        return f"The current price of {ticker} is ${stock.info.get('currentPrice', 'N/A')}"
    except Exception as e:
        return f"Error fetching stock price: {e}"

# Function to fetch recent stock news
def get_recent_stock_news(ticker):
    """
    Fetch recent news articles about the given stock ticker.

    Args:
        ticker: The stock ticker symbol.

    Returns:
        A list of news article summaries.
    """
    try:
        search_url = f"https://www.google.com/search?q={ticker}+stock+news"
        search = DuckDuckGoSearchRun()
        return search.run(search_url)
    except Exception as e:
        return f"Error fetching news: {e}"

# Function to get financial statements
def get_financial_statements(ticker):
    """
    Fetch financial statements for the given stock ticker.

    Args:
        ticker: The stock ticker symbol.

    Returns:
        A dictionary containing financial statement data.
    """
    try:
        stock = yf.Ticker(ticker)
        return stock.financials.to_dict()
    except Exception as e:
        return f"Error fetching financial statements: {e}"

# Initialize LangChain Tools
search = DuckDuckGoSearchRun()

tools = [
    Tool(
        name="Get Stock Data",
        func=get_stock_price,
        description="Fetches stock price using Yahoo Finance. Input the stock ticker."
    ),
    Tool(
        name="Web Search",
        func=search.run,
        description="Fetches recent stock-related news using DuckDuckGo."
    ),
    Tool(
        name="Get Recent News",
        func=get_recent_stock_news,
        description="Fetches recent news about stocks."
    ),
    Tool(
        name="Get Financial Statements",
        func=get_financial_statements,
        description="Fetches financial statements of a company using Yahoo Finance."
    )
]

# Initialize LangChain Agent
zero_shot_agent = initialize_agent(
    llm=OpenAI(temperature=0),
    agent="zero-shot-react-description",
    tools=tools,
    verbose=True,
    max_iterations=4,
    return_intermediate_steps=True,
    handle_parsing_errors=True
)

# Run the agent
if __name__ == "__main__":
    question = input("Enter your stock market question: ").strip()
    response = zero_shot_agent(question)
    print(response)

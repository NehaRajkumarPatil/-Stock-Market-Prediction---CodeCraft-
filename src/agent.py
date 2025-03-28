import os
from langchain.agents import initialize_agent
from langchain.tools import Tool
from langchain.llms import OpenAI
from langchain.tools import DuckDuckGoSearchRun
import yfinance as yf

# Set API Key
os.environ["OPENAI_API_KEY"] = "your_api_key"

# Function to fetch stock prices
def get_stock_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        return f"The current price of {ticker} is ${stock.info.get('currentPrice', 'N/A')}"
    except Exception as e:
        return f"Error: {e}"

# Initialize DuckDuckGo search
search = DuckDuckGoSearchRun()

# Define tools for the agent
tools = [
    Tool(
        name="get_stock_price",
        func=get_stock_price,
        description="Fetch stock price using Yahoo Finance."
    ),
    Tool(
        name="web_search",
        func=search.run,
        description="Use DuckDuckGo to fetch stock-related news."
    )
]

# Initialize LangChain agent
zero_shot_agent = initialize_agent(
    llm=OpenAI(temperature=0),
    agent="zero-shot-react-description",
    tools=tools,
    verbose=True
)

if __name__ == "__main__":
    question = input("Ask your stock market question: ")
    print(zero_shot_agent(question))

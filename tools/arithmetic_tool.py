import os
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_community.utilities.alpha_vantage import AlphaVantageAPIWrapper
load_dotenv()

@tool
def multiply(x: int, y: int) -> int:
    """
    Multiply two integers

    Args:
        x (int): First integer.
        y (int): Second integer.
    
    Return:
        int: Product of x and y.
    """
    return x*y

@tool
def add(x: int, y: int) -> int:
    """
    Adds two integers

    Args:
        x (int): First integer.
        y (int): Second integer.
    
    Return:
        int: Sum of x and y.
    """
    return x+y

@tool
def currency_converter(from_curr: str, to_curr: str, value: float)->float:
    os.environ["ALPHAVANTAGE_API_KEY"] = os.getenv('ALPHAVANTAGE_API_KEY')
    alpha_vantage = AlphaVantageAPIWrapper()
    response = alpha_vantage._get_exchange_rate(from_curr, to_curr)
    exchange_rate = response['Realtime Currency Exchange Rate']['5. Exchange Rate']
    return value * float(exchange_rate)
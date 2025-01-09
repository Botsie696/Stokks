import yfinance as yf
def convert_to_readable(num):
    """
    Convert large numbers to a more readable format.

    Args:
        num (float): The number to be converted.

    Returns:
        str: The number in a more readable format.
    """

    if num >= 1e9:
        return f"{num / 1e9:.2f} billion"
    elif num >= 1e6:
        return f"{num / 1e6:.2f} million"
    elif num >= 1e3:
        return f"{num / 1e3:.2f} thousand"
    else:
        return str(num)

# Example usage:
numbers = [9.293658e7, 1.23456789e9, 12345, 67890]

def get_price_target(ticker):
    """
    Retrieves the price target for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        dict: A dictionary containing the price target data.
    """
    stock = yf.Ticker(ticker)
    data = yf.download(ticker, period="1mo")
    info = stock.info
    average_volume = data['Volume'].mean()
    print(convert_to_readable(int(average_volume)))
    
    # Check if price target data is available
    if 'targetMeanPrice' in info and 'targetHighPrice' in info and 'targetLowPrice' in info:
        return {
            'mean': info['targetMeanPrice'],
            'high': info['targetHighPrice'],
            'low': info['targetLowPrice'] , 


        }
    
        
    else:
        return None

# Example usage
ticker = 'NNOX'
price_target = get_price_target(ticker) 
    # Get ticker data

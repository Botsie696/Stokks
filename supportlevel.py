import yfinance as yf
import pandas as pd

# Define the ticker symbol and the period
months = 3
ticker = "LBRT"  # Replace with your desired ticker symbol
period = f"{months}mo"  # The last month of data
ticker = yf.Ticker(ticker)
# Download the historical data


# Get the minimum closing price within the last month
def SupportLevel(data=None , beta=None):
    if (data is None):
        print("Not here")
        data = ticker.history(period=f"{months}mo" , interval ='5d' )
        start_date = "2024-08-01"
        end_date = "2024-10-17"

        # Fetch historical data
        # data = ticker.history(start=start_date, end=end_date, interval='5d')

    
    support_price = data['Close'].min()
    
    BreakoutLevel = data['Close'].mean()
    price_changes = data['Close'].pct_change().mean()
  
    # print(currentPrice)
    BreakoutLevelVolume = data['Volume'].median()
    BreakoutLevelVolumeHigh = data['Volume'].mean()
    calc = BreakoutLevelVolumeHigh / BreakoutLevelVolume 
    BreakoutMeans = support_price / BreakoutLevel
    # print(calc  , BreakoutMeans , price_changes)
    BreakoutLevelCalc = (BreakoutLevel / 100) * ((calc + BreakoutMeans + (price_changes * 10) * (beta / 2)) * 10)

    BreakoutLevelCalc = (BreakoutLevel + BreakoutLevelCalc)

    BreakoutLevel = round(BreakoutLevel , 2)
    BreakoutLevelCalc = round(BreakoutLevelCalc , 2)
    # Print the current price and estimated support price
    
    
    return BreakoutLevel , BreakoutLevelCalc

price , breakout = SupportLevel(beta=1.72);
print(price , breakout , 1)
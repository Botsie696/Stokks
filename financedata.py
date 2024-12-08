import yfinance as yf
import datetime
import re
import pandas as pd
import numpy as np 
from yahooquery import search
from dateutil.relativedelta import relativedelta
import dataprovider
def AnalyseWithYahoo(data, Repeast=False):
    try:
        
        # Clean the input stock symbol
        stock_symbol = re.sub(r"['\"\-\\\.]", "", data).strip()
        
        # Define date range
        end_date = datetime.datetime.today()
        start_date = end_date - datetime.timedelta(days=dataprovider.Months*30)  # Approx 6 months
        
        # Fetch historical data
        stock_data = yf.download(stock_symbol, start=start_date, end=end_date, progress=False)
        # print(stock_data)
        
        # Check if data is empty
        if stock_data.empty:
            if not Repeast:
                # print(f"No data found for symbol '{stock_symbol}'. Attempting to search by company name...")
                new_symbol = SearchSymbol(data)
                if new_symbol == "NONE":
                    # print(f"Unable to find a symbol for '{data}'.")
                    return "NONE"  , "NONE"  , stock_symbol
                return AnalyseWithYahoo(new_symbol, Repeast=True)
            else:
                # print(f"Error: No data found even after symbol search for '{data}'.")
                return "NONE" , "NONE" , stock_symbol
        
        # Ensure data is sorted by date
        stock_data.sort_index(inplace=True)

        # Extract first and last close prices as scalars
        try:
            first_close = float(stock_data['Close'].iloc[0])  # Convert to scalar
            last_close = float(stock_data['Close'].iloc[-1])  # Convert to scalar
        except IndexError:
            # print(f"Error: Insufficient data for symbol '{stock_symbol}'.")
            return "NONE"  , "NONE" , stock_symbol
        
        # Calculate price rise and percentage rise
        price_rise = last_close - first_close
        CurrentPrice = str(f"{last_close:.2f}")
         
        
        percentage_rise = (price_rise / first_close) * 100
        
        # Display results
        # print(f"{data} ({stock_symbol}): Approximate rise in price: {price_rise:.2f}")
        # print(f"{data} ({stock_symbol}): Percentage rise: {percentage_rise:.2f}%")
        return round(percentage_rise , 2) , CurrentPrice , stock_symbol
    
    except Exception as e:
        if not Repeast:
            new_symbol = SearchSymbol(data)
            if new_symbol == "NONE":
                return "NONE" , "NONE" , "n/a"
            return AnalyseWithYahoo(new_symbol, Repeast=True)
        # print(f"An error occurred while processing symbol '{data}': {e}")
        return "N/A"  , "n/a"  , "n/a"

def SearchSymbol(company_name):
    try:
        # print(f"Searching for symbol for company name: '{company_name}'")
        results = search(company_name)
        for result in results.get("quotes", []):
            if 'symbol' in result:
                # print(f"Found symbol: {result['symbol']} for company: {result['longname']}")
                return result['symbol']
        # print(f"No symbol found for company name: '{company_name}'")
        return find_stock_ticker(company_name)
    except Exception as e:
        # print(f"Error occurred during symbol search for '{company_name}': {e}")
        return "NONE"
    

def GetPriceOf(Stock):
    # Get the current date and adjust for possible stock market hours
   
    Stock = re.sub(r"['\"\-\\\.]", "", Stock).strip()
    # print("Stock is " + Stock)
    today = datetime.datetime.today()
    start_date = today - datetime.timedelta(days=5)  # Look back a few days to ensure data retrieval
    stock_data = yf.download(Stock, start=start_date, end=today, progress=False)
    stock_data.sort_index(inplace=True)
    if stock_data.empty:
        raise ValueError(f"No data found for stock: {Stock}")
    
    last_close = round(float(stock_data['Close'].iloc[-1]), 2)
    return last_close
# Example usage

def GetRevenue(Stock):
    try:
        # Clean the input stock symbol
        Stock = re.sub(r"['\"\-\\\.]", "", Stock).strip()
        
        # Fetch company metadata to get revenue
        ticker = yf.Ticker(Stock)

        # Attempt to fetch stock information
        try:
            stock_info = ticker.info
        except Exception as e:
            return f"N/A"

        # Extract revenue (if available)
        revenue = stock_info.get("totalRevenue", None)  # Revenue is in raw numbers (e.g., USD)
        if revenue is None:
            return f"Revenue data not available for {Stock}."
        else:
            # Convert revenue to billions or millions for readability
            if revenue >= 1e9:
                return f"${revenue / 1e9:.2f} B"
            elif revenue >= 1e6:
                return f"${revenue / 1e6:.2f} M"
            else:
                return f"${revenue:.2f}"

    except Exception as e:
        # Catch all other errors
        return f"n/a"
    
def ConsistancyScore(Stock , Months , Distance = 15):
    
    Score = 0
    Stock = re.sub(r"['\"\-\\\.]", "", Stock).strip()
    # Download the stock data
    end_date = datetime.datetime.today() 
    start_date = end_date - datetime.timedelta(days=Months*30)  # Approx 6 months
    stock_data = yf.download(Stock, start=start_date, end=end_date, progress=False)

# Resample to get the closing stock price every 15 days
    closing_15_days = stock_data['Close'].resample(f'{Distance}D').last()
    prices_only = closing_15_days.values.tolist()
    if not prices_only:
        return "NONE"  , "NONE" , "NONE" , "NONE"
    prev = float(prices_only[0][0])
    Total = 0
    AverageIncrease = 0
    PercentageChanges = []
    for close in prices_only:
        
        price = float(close[0])
        price_rise = price - prev
        percentage_rise = (price_rise / prev) * 100
        AverageIncrease += percentage_rise
        if (percentage_rise > 0):
            Score += 1
            
        prev = price
        Total += 1
        PercentageChanges.append(percentage_rise)
    
    Average = round(AverageIncrease / Total, 2)
    # print("Average: " + str(Average))  # Rounds to 2 decimal places
    median_percentage_change = np.median(PercentageChanges)
    MEd = round(median_percentage_change, 2)
    # print("Median: " + str(MEd))  # Rounds to 2 decimal places
    ScoresMids = round(Score / Total, 2)
    return str(f"{str(Score)}/{str(Total)}")  , Average , MEd  , ScoresMids
        
        


def find_stock_ticker(company_name):
    # Search for the company using yfinance's Ticker search feature
    try:
        search_results = yf.Ticker(company_name)
        return search_results.ticker if search_results.ticker else "N/A"
    except Exception as e:
        return f"Error occurred: {e}"
    
# print(AnalyseWithYahoo("AI"))

# print("TOKL" + find_stock_ticker("TESLA"))
# print(ConsistancyScore("tesla" , 6 , Distance=5))
# print(ConsistancyScore("PLTR" , 6 , Distance=5))
# print(ConsistancyScore("PSIX" , 6 , Distance=5))
# print(ConsistancyScore("VOO" , 6 , Distance=5))
# print(GetRevenue("PLTR"))
# Price watcher of all the stocks, checks price and gives rates 
# Edit youtube links search 
# chat ai with data as all the transcripts without bulletpoints
# Revenue 
# For summary ask chatgpt to give summary for eachs stock seperated by +++
# Check for revenue growth 

# buy PSIX & sell microstrategy buy pltr as well for rest and (APLD) APPLIED BACKCHAIN 
# Consider HIMS

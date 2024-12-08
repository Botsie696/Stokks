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
dis = 5
mons = 1
# print("TOKL" + find_stock_ticker("TESLA"))
print(ConsistancyScore("SOFI" , mons , Distance=dis) , "SOFI")
print(ConsistancyScore("HIMS" , mons , Distance=dis) , "HIMS")
print(ConsistancyScore("HUT" , mons , Distance=dis) , "HUT")
print(ConsistancyScore("APP" , mons, Distance=dis) ,"APP")
print(ConsistancyScore("BTDR" , mons , Distance=dis) , "BTDR")

Average = 0
Median = 0

Comp = ["SOFI"  , "APP" , "BTDR"]
AverageSC = []
MedianSC = []
GrowthSc = []
for n in Comp:
    growth, average, median , score = ConsistancyScore(n , mons, Distance=dis)
    Average += average
    Median += median
    AverageSC.append(average)
    MedianSC.append(median)
    GrowthSc.append(growth)
k = 0
for n in Comp:
    Avg = AverageSC[k] / max(AverageSC)
    Med = MedianSC[k] / max(MedianSC)
    numerator, denominator = map(int, GrowthSc[k].split('/'))

# Perform the division
    result = numerator / denominator
    print( n  , round((Avg + Med + result) , 2) , GrowthSc[k])
    k += 1



# growth , average, mid, score
# BTDR 
# HUT
# APP
# HIMS
# SOFI

# APP - BTDR - HUT - SOFI - HIMS

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


# SOFI 0.76 3/6 = 2.96 + .5 + .25 = 3.46 - Buy
# APP 1.48 4/6 = 3.63 + 1 = 4.63 - strong buy
# BTDR 2.63 5/6 = 3.58 - .5 = 3.08 - strong buy 

import yfinance as yf

 


# BTDR 2.63 5/6 = 3.58 - .5 = 3.08 - strong buy 
def GetEstimatePrice(StockName):
# Specify the stock ticker
    ticker = StockName  # Replace with the stock ticker you're interested in

    # Fetch the stock data
    stock = yf.Ticker(ticker)

    # Get valuation metrics
    info = stock.info

    # Extract relevant details
    valuation_measures = {
        "Market Cap": info.get("marketCap"),
        "Enterprise Value": info.get("enterpriseValue"),
        "Trailing P/E": info.get("trailingPE"),
        "Forward P/E": info.get("forwardPE"),
        "PEG Ratio (5yr expected)": info.get("pegRatio"),
        "Price/Sales (ttm)": info.get("priceToSalesTrailing12Months"),
        "Price/Book (mrq)": info.get("priceToBook"),
        "Enterprise Value/Revenue": info.get("enterpriseToRevenue"),
        "Enterprise Value/EBITDA": info.get("enterpriseToEbitda"),
    }

    # Extract Financial Highlights
    financial_highlights = {
        "Profit Margin": info.get("profitMargins"),
        "Return on Assets (ttm)": info.get("returnOnAssets"),
        "Return on Equity (ttm)": info.get("returnOnEquity"),
        "Revenue (ttm)": info.get("totalRevenue"),
        "Net Income Avi to Common (ttm)": info.get("netIncomeToCommon"),
        "Diluted EPS (ttm)": info.get("trailingEps"),
        "Total Cash (mrq)": info.get("totalCash"),
        "Total Debt/Equity (mrq)": info.get("debtToEquity"),
        "Levered Free Cash Flow (ttm)": info.get("freeCashflow"),
    }

    # Extract Market Sentiment Metrics
    market_sentiment = {
        "Avg Vol (3 month)": info.get("averageVolume"),
        "Avg Vol (10 day)": info.get("averageDailyVolume10Day"),
        "Shares Outstanding": info.get("sharesOutstanding"),
        "Float": info.get("floatShares"),
        "Held by Insiders (%)": info.get("heldPercentInsiders"),
        "Held by Institutions (%)": info.get("heldPercentInstitutions"),
        "Short % of Float": info.get("shortPercentOfFloat"),
        "Short Ratio": info.get("shortRatio"),
    }

    # Format and display the output
    # print("Financial Highlights:")
    for key, value in financial_highlights.items():
        if isinstance(value, (float, int)):
            value = f"{value:,.2f}"
        # print(f"{key}: {value}")

    # print("\nMarket Sentiment Metrics:")
    for key, value in market_sentiment.items():
        if isinstance(value, (float, int)):
            value = f"{value:,.2f}"
        # print(f"{key}: {value}")

    # Define the price estimation logic
    def estimate_price(market_cap, shares_outstanding, adjustments=1):
        if not market_cap or not shares_outstanding:
            return "Data unavailable"
        estimated_price = (market_cap / shares_outstanding) * adjustments
        return round(estimated_price, 2)

    # Simulate shares outstanding
    shares_outstanding = market_sentiment.get("Shares Outstanding", 1e10)  # Replace with real data

    # Estimate adjustments based on metrics
    adjustments = 1

    # Incorporate Financial Highlights
    if financial_highlights["Profit Margin"] and financial_highlights["Profit Margin"] < 0:
        adjustments *= 0.8
    if financial_highlights["Return on Equity (ttm)"] and financial_highlights["Return on Equity (ttm)"] > 0.15:
        adjustments *= 1.1

    # Incorporate Market Sentiment
    if market_sentiment["Short % of Float"] and market_sentiment["Short % of Float"] > 10:
        adjustments *= 0.9  # Penalize for high short interest
    if market_sentiment["Held by Institutions (%)"] and market_sentiment["Held by Institutions (%)"] > 50:
        adjustments *= 1.1  # Reward for institutional confidence
    if market_sentiment["Avg Vol (10 day)"] and market_sentiment["Avg Vol (3 month)"]:
        if market_sentiment["Avg Vol (10 day)"] > market_sentiment["Avg Vol (3 month)"]:
            adjustments *= 1.05  # Reward for increasing trading activity
    if valuation_measures["Trailing P/E"] and valuation_measures["Trailing P/E"] > 50:
        adjustments *= 0.95  # Penalize for high P/E
    if valuation_measures["Enterprise Value/Revenue"] and valuation_measures["Enterprise Value/Revenue"] > 10:
        adjustments *= 0.9  # Penalize for high EV/Revenue
    # # adjustments *= 5.02
 

   
    # Calculate the estimated price
    estimated_price = estimate_price(valuation_measures["Market Cap"], shares_outstanding, adjustments)
    
    # Print valuation measures and price estimate
    # print("\nValuation Measures:")
    for key, value in valuation_measures.items():
        if isinstance(value, (float, int)):
            value = f"{value:,.2f}"
        # print(f"{key}: {value}")
    prc = float(GetPriceOf(StockName))
    print(prc)
    Price =  1 - round((prc / estimated_price) , 2)
    
    # print("Upd" , round(Price , 2))
    # print(f"\nEstimated Price: ${estimated_price}")
# Retrieve the latest recommendations
    recommendations = stock.recommendations
    # Process the recommendations
    most_recommended = ""
    if recommendations is not None and not recommendations.empty:
        # print("Recent Analyst Recommendations:")
        # print(recommendations.tail(300))  # Display the last 10 recommendations

        # Aggregate totals for recommendation columns
        recommendation_summary = recommendations[["strongBuy", "buy", "hold", "sell", "strongSell"]].sum()

        # Find the most recommended rating
        most_recommended = recommendation_summary.idxmax()

        # print(f"\nThe most recommended rating is: {most_recommended} with a total count of {most_recommended_count}.")
    

    return float(estimated_price) , most_recommended
 


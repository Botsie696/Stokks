import yfinance as yf
import requests
from lxml import html
import re
import numpy as np

import financedata
# Get earnings data
def StockEarnings(stock):
    try:
        earnings_data = stock.earnings_history
        # 2.35 - 2.18
        # print(earnings_data)
        
        numeric_eps_diff_values = [value for value in earnings_data['epsDifference'].tolist() if isinstance(value, (int, float)) and not np.isnan(value)][2:]
        numeric_surprise_values = [value for value in earnings_data['surprisePercent'].tolist() if isinstance(value, (int, float)) and not np.isnan(value)][2:]
        # Calculate sums
        EpsDiff = round(sum(numeric_eps_diff_values), 2)
        Surprise = round(sum(numeric_surprise_values), 2)
 
        # print(Eps,  Surprise)
        # print(earnings_data)
        return EpsDiff, Surprise 
    except Exception as e:
        # print("pass" + str(e))
        return 1 , 1
#  price targets , how high will it reach , hype around it 
def calculate_percent_changes(arr):
    """
    Calculate the percent changes between consecutive numbers.

    Args:
        arr (list): A list of numbers.

    Returns:
        list: A list of percent changes.
    """
    if len(arr) < 2:
        raise ValueError("Array must have at least two elements")

    percent_changes = []
    for i in range(1, len(arr)):
        previous_value = arr[i-1]
        current_value = arr[i]
        percent_change = ((current_value - previous_value) / previous_value) * 100
        percent_changes.append(percent_change)
    changes = []
    for i, change in enumerate(percent_changes):
        changes.append(change)
    x = 0
    for n in changes:
        x += n
    
    return x / len(changes)
def calculate_average(dictionary):
    """
    Calculate the average of a dictionary with string keys and mixed-type values.
    Args:
        dictionary (dict): A dictionary with string keys and mixed-type values.
    Returns:
        float: The average value of the numeric values in the dictionary.
    """
    numeric_values = [value for value in dictionary if isinstance(value, (int, float))]
    total = sum(numeric_values)
    count = len(numeric_values)
    if (count == 0):
        return count
    return total / count
def ConsistancyScore(Stock, Months, Distance=15):
    

    # Fetch historical stock prices
    ticker = yf.Ticker(Stock)
    if not ticker.info or 'symbol' not in ticker.info or not ticker.info['symbol']:
            print(f"Ticker '{Stock}' does not exist.")
            Name = financedata.SearchSymbol(Stock)
            ticker = yf.Ticker(Name)
            
    print(ticker)
    hist = ticker.history(period=f"{Months}mo")
    # hist = ticker.history(start='2024-10-01', end='2024-12-18')

    # Calculate daily price changes
    price_changes = hist['High'].pct_change()

    # Extract required metrics
    avg_price_change = price_changes.mean()
    med_price_change = price_changes.median()

    # Prepare daily prices list
    daily_prices = hist['Close'].reset_index().rename(columns={'index': 'Date', 'Close': 'Price'})

    # Initialize score and collect medians
    score = 0
    meds = []
    total = len(price_changes)

    for i in range(3, total):
        current_price = daily_prices.loc[i, 'Price']

        if price_changes.iloc[i] > 0 and current_price > daily_prices.loc[i - 3, 'Price']:
            score += 1

        # Penalize for consistent downward movement
        if (price_changes.iloc[i] < 0 and price_changes.iloc[i - 2] < 0 and price_changes.iloc[i - 3] < 0):
            score -= 1
        elif (i > 6 and current_price < daily_prices.loc[i - 6, 'Price']):
            score -= 1
        elif (i > Distance and current_price < daily_prices.loc[i - Distance, 'Price']):
            score -= 1

        # Collect median prices at intervals
        if i % 10 == 0:
            meds.append(current_price)
    Price = 0
    if (total > 0):
        Price = round(daily_prices.loc[total-1, 'Price'],2)
    # Calculate percentage change from collected medians
    perk = calculate_percent_changes(meds) if len(meds) >= 2 else 0

    # Retrieve earnings data
    eps, surprise = StockEarnings(ticker)

    recommendations = ticker.recommendations
        # Process the recommendations
    most_recommended = ""
    if recommendations is not None and not recommendations.empty:
        # print("Recent Analyst Recommendations:")
        # print(recommendations.tail(300))  # Display the last 10 recommendations

        # Aggregate totals for recommendation columns
        recommendation_summary = recommendations[["strongBuy", "buy", "hold", "sell", "strongSell"]].sum()

        # Find the most recommended rating
        most_recommended = recommendation_summary.idxmax()

    
    # print(Stock , Price)
    # Return computed values
    return (
        perk,
        round((avg_price_change * 100) * 30, 2),
        round((med_price_change * 100) * 30, 2),
        f"{score}/{total}",
        round(score, 2),
        eps,
        surprise , 
        Price , 
        most_recommended
    )


months = 3

Scores = {}



def calculate_weighted_scores(stock_symbols, months):
    StoreData = {}
    
    for n in stock_symbols:
        consistency_score, avg_price_change, med_price_change, scores_mids, Sore, Eps, Surprise , price , recommendations = ConsistancyScore(n, months)
        
        if med_price_change > 0 and avg_price_change > 0:
            StoreData[n] = {
                'Mid': med_price_change,
                'Avg': round(avg_price_change,2),
                'Sore': Sore,
                'Consis': consistency_score,
                'Eps': Eps,
                'Surprise': Surprise, 
                'Growth Rate': scores_mids, 
                'Price': price, 
                'recommendation' : recommendations
            }

    if not StoreData:
        return {}

    # Extract relevant data in a single step
    medians = [data['Mid'] for data in StoreData.values()]
    averages = [data['Avg'] for data in StoreData.values()]
    scores_incr = [data['Sore'] for data in StoreData.values()]
    streak_month = [data['Consis'] for data in StoreData.values()]

    # Calculate averages only once
    highestMid = calculate_average(medians)
    highestAvg = calculate_average(averages)
    highestSStore = calculate_average(scores_incr)
    highestConsis = calculate_average(streak_month)

    Scores = {}

    for n, data in StoreData.items():
        WeightMid = data['Mid'] / highestMid
        WeightAvg = data['Avg'] / highestAvg
        WeightIncr = data['Sore'] / highestSStore
        WeightConsis = data['Consis'] / highestConsis
        WeightEps = 2 if data['Eps'] > 0 else 0
        WeightSurp = 2 if data['Surprise'] > 0 else -1

        if WeightMid > 0:
            Scores[n] = round((WeightMid * 2) + (WeightAvg * 0.68) + (WeightIncr * 2) + WeightConsis + (WeightEps * 3) + (WeightSurp * 2), 2)
        else:
            print(n , "LOW EPS")
    return sorted(Scores.items(), key=lambda item: item[1]) , StoreData

# Example usage
# sorted_scores = calculate_weighted_scores(stock_symbols, months)
# print(sorted_scores)




def WriteToFileAverage(stock_symbols , file_path):
        
        sorted_dict , StoreData = calculate_weighted_scores(stock_symbols , 3)
       
        # print("Dicted")
        # print(sorted_dict)
        print("Writing to File")
        with open(file_path, "w") as file:
            for key, value in sorted_dict:
                
                # Name, Score,Price, Median, Average, Sore, Eps, Surprise, Growth Rate , Rec
                file.write(
                    f"{key},{value},{StoreData[key]['Mid']},"
                    f"{StoreData[key]['Avg']},{StoreData[key]['Sore']},{StoreData[key]['Eps']},{StoreData[key]['Surprise']},{StoreData[key]['Growth Rate']},{StoreData[key]['recommendation']}\n"
                    )
        
 
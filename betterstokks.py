import yfinance as yf
import requests
from lxml import html
import re
import numpy as np
import financedata
from requests.exceptions import HTTPError
import time


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
    # Extract numeric values from the dictionary
    numeric_values = [value for value in dictionary if isinstance(value, (int, float))]
    
    # Sort the numeric values in descending order
    numeric_values.sort(reverse=True)
    
    # Calculate the top 30% threshold
    top_30_percent_count = max(1, int(len(numeric_values) * 0.3))  # Ensure at least one value is included
    
    # Take the top 30% of numeric values
    top_30_percent_values = numeric_values[:top_30_percent_count]
    
    # Calculate the average
    if not top_30_percent_values:
        return 0  # Avoid division by zero if no numeric values are found
    
    total = sum(top_30_percent_values)
    count = len(top_30_percent_values)
    return total / count

def ConsistancyScore(Stock, Months, Distance=15):
    
    try:
        # Fetch historical stock prices
       
        ticker = yf.Ticker(Stock)
        fifty_two_week_low = ticker.info.get("fiftyTwoWeekLow")
        fifty_two_week_high = ticker.info.get("fiftyTwoWeekHigh")
        if not ticker.info or 'symbol' not in ticker.info or not ticker.info['symbol']:
                print(f"Ticker '{Stock}' does not exist.", ticker)
                
                Name = financedata.SearchSymbol(Stock)
                ticker = yf.Ticker(Name)
                # if ()
                
                print("Name is still an ussue" + str(Name))
                
                
        hist = ticker.history(period=f"{Months}mo" )
        # hist = ticker.history(start='2024-10-01', end='2024-12-18')
        
        # print("===", str(hist) , "Histroou")
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
        PriceChangeMonth = 0
        currentPrice =  daily_prices.loc[(total-1), 'Price']
        if (total > 30):
            PriceChangeMonth = round((1 - (daily_prices.loc[(total-30), 'Price'] / currentPrice)) * 100,2)
        PriceChangeFromHigh52 = round(1 - (currentPrice / fifty_two_week_high), 2)
        
        print(Stock , "Price change: " + str(PriceChangeFromHigh52 * 100))
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
            most_recommended , f"{fifty_two_week_low}-{fifty_two_week_high}" , 
            PriceChangeMonth , PriceChangeFromHigh52
        )
    except HTTPError as e:
            if e.response.status_code == 429:  # Too many requests
                print("Rate limit hit. Retrying...")
                time.sleep(10)
    except Exception as e:
        if ("429" in str(e)):
            print("This is an major")
        print("ME+ majorjob -", e, "ME+-")
        return None

months = 3

Scores = {}


def get_proxies_from_api():
    url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=US"
    response = requests.get(url)
    proxies = response.text.splitlines()
    return proxies

# Convert proxies to the required format
def convert_to_proxy_list(proxies):
    proxy_list = []
    for proxy in proxies:
        proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        proxy_list.append(proxy_dict)
    return proxy_list

def validate_proxy(proxy):
    url = "http://httpbin.org/ip"  # Simple endpoint to test proxy
    try:
        response = requests.get(url, proxies=proxy, timeout=5)
        if response.status_code == 200:
            print(f"Proxy {proxy} is valid")
            return True
    except Exception as e:
        print(f"Proxy {proxy} failed: {e}")
    return False



# Fetch and convert proxies
def proxiesList():
    proxies_raw = get_proxies_from_api()
    proxies = convert_to_proxy_list(proxies_raw)
    newProxy = []
    for n in proxies:
        item = validate_proxy(n)
        if (item):
            newProxy.append(n)
        if len(newProxy) >= 3:
            break;
    proxies = newProxy
    return proxies


def calculate_weighted_scores(stock_symbols, months,timer=False ):
    StoreData = {}
    
    proxy_index = 0
    proxy = None
    proxies = []
    value = 0
     
    if (timer):
        proxies = proxiesList()

    for n in stock_symbols:
        value += 1
        
        # time.sleep(2)
      
        if (timer==True):
            if value % 10 == 0 and value > 0:
                proxy_index = (proxy_index + 1) % len(proxies)
                proxy = proxies[proxy_index]
                session = requests.Session()
                session.proxies = proxies
                
                yf.shared._requests = proxy
                time.sleep(10)
                print(f"Switching to proxy: {proxies[proxy_index]}")
            # time.sleep(2)
        
        gotcha = ConsistancyScore(n, months)
        if (gotcha == None):
            # value += 1
            continue
        (consistency_score, avg_price_change, med_price_change, scores_mids, Sore, Eps, Surprise , price , recommendations , weeksHL , PriceChangeMonth , PriceChangeFromHigh52) = gotcha
        
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
                'recommendation' : recommendations , 
                '52WeekLowHigh' : weeksHL , 
                'PriceChangeMonth' : PriceChangeMonth , 
                'PriceChangeFromHigh52' : PriceChangeFromHigh52
            }

    if not StoreData:
        return {}

    # Extract relevant data in a single step
    medians = [data['Mid'] for data in StoreData.values()]
    averages = [data['Avg'] for data in StoreData.values()]
    scores_incr = [data['Sore'] for data in StoreData.values()]
    streak_month = [data['Consis'] for data in StoreData.values()]
    MonthAvgRise = [data['PriceChangeMonth'] for data in StoreData.values()]

    # Calculate averages only once
    highestMid = calculate_average(medians)
    highestAvg = calculate_average(averages)
    highestSStore = calculate_average(scores_incr)
    highestConsis = calculate_average(streak_month)
    highestAvgRise = calculate_average(MonthAvgRise)
    
    Scores = {}

    for n, data in StoreData.items():
        WeightMid = data['Mid'] / highestMid
        WeightAvg = data['Avg'] / highestAvg
        WeightIncr = data['Sore'] / highestSStore
        WeightConsis = data['Consis'] / highestConsis
        WeightAvgMonthrise = data['PriceChangeMonth'] / highestAvgRise
        WeightEps = 1 if data['Eps'] > 0 else 0
        WeightSurp = 1 if data['Surprise'] > 0 else -1
        print(WeightMid , WeightAvg , WeightIncr , WeightConsis , WeightEps , WeightSurp)
        if WeightMid > 0:
            Scores[n] = round((WeightMid * 1.8) + (WeightAvg * 0.68) + (WeightIncr * 1) + WeightConsis + (WeightEps * 1.1) + (WeightSurp * 1) + (WeightAvgMonthrise * 1.5), 2)
        else:
            print(n , "LOW EPS")
    return sorted(Scores.items(), key=lambda item: item[1]) , StoreData


# # Example usage
# value = 0
# for n in range(1,5000):
#     sorted_scores = calculate_weighted_scores(['RDDT' , 'PLTR' , 'QUBT'], months, value=n+4 , timer=True)
#     # print(sorted_scores)
#     print(n)

# sorted_scores = calculate_weighted_scores(['QUBT','ALAB' ,'RGTI'], months)
# print(sorted_scores)

def WriteToFileAverage(stock_symbols , file_path,timers=False):
        
        sorted_dict , StoreData = calculate_weighted_scores(stock_symbols , 3,timer=timers)
       
        # print("Dicted")
        # print(sorted_dict)
        print("Writing to File")
        with open(file_path, "w") as file:
            for key, value in sorted_dict:
                
                # Name, Score,Price, Median, Average, Sore, Eps, Surprise, Growth Rate , Rec
                file.write(
                    f"{key},{value},{StoreData[key]['Price']},{StoreData[key]['Mid']},"
                    f"{StoreData[key]['Avg']},{StoreData[key]['Sore']},{StoreData[key]['Eps']},{StoreData[key]['Surprise']},{StoreData[key]['Growth Rate']},{StoreData[key]['recommendation']},{StoreData[key]['52WeekLowHigh'],{StoreData[key]['PriceChangeMonth'],{StoreData[key]['PriceChangeFromHigh52']}}}\n"
                    )
        
 
 # Function to fetch proxies from the API


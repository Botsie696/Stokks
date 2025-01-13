import yfinance as yf
import requests
from lxml import html
import re
import math
import numpy as np
import financedata
from requests.exceptions import HTTPError
import time
import buytime

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
    top_30_percent_count = max(1, int(len(numeric_values) * 0.4))  # Ensure at least one value is included
    
    # Take the top 30% of numeric values
    top_30_percent_values = numeric_values[:top_30_percent_count]
    
    # Calculate the average
    if not top_30_percent_values:
        print("Total")
        return 1  # Avoid division by zero if no numeric values are found
  
    total = sum(top_30_percent_values)
    count = len(top_30_percent_values)
    if (total / count == 0): 
        print("NOT" , total , count)
        return 1
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
                
                # print("Name is still an ussue" + str(Name))
        
        # was three months 
        hist = ticker.history(period=f"{Months}mo" , interval ='5d' )
        # hist = ticker.history(start='2024-12-15', end='2025-01-05' , interval='5d')
        # hist = yf.download(ticker, period="1mo", interval="1d")
       
        # print("===", str(hist) , "Histroou")
        # Calculate daily price changes
        sector = ticker.info.get("sector", "N/A")
        industry = ticker.info.get("industry", "N/A")
        
        beta = ticker.info.get("beta", "N/A")
        price_changes = hist['Close'].pct_change()
        betaAddition = 0
        if (beta != 'N/A' and beta > 0):
            betaAddition = (Months * 30) / 5
            betaAddition = beta / betaAddition
        else:
            beta = 1
        # Extract required metrics
        avg_price_change = price_changes.mean()
        med_price_change = price_changes.median()
        
        med_price_change = ((betaAddition/2) + med_price_change)
        # Prepare daily prices list
        daily_prices = hist['Close'].reset_index().rename(columns={'index': 'Date', 'Close': 'Price'})

        # Initialize score and collect medians
        score = 0
        meds = []
        total = len(price_changes)

        for i in range(0, total):
            current_price = daily_prices.loc[i, 'Price']

            if i > 2 and price_changes.iloc[i] > 0 and current_price > daily_prices.loc[i - 2, 'Price']:
                score += 1
            if i > 1 and price_changes.iloc[i] > 0 and current_price > daily_prices.loc[i - 1, 'Price']:
                score += 1

            # Penalize for consistent downward movement
            if i > 2 and (price_changes.iloc[i] < 0 and price_changes.iloc[i - 1]):
                score -= min(1 / beta , 1)
               
            if (i > 6 and (current_price < daily_prices.loc[i - 6, 'Price'])):
                score -= min(1 / beta , 1)

            elif (i > Distance and (current_price < daily_prices.loc[i - Distance, 'Price'])):
                score -= min(1 / beta , 1)
            
            if (i > 1):
                p = 1 - (current_price / daily_prices.loc[i - 1, 'Price']) 
                p *= 100
                if (p > 10):
                    score -= min(2 / beta , 2)
                elif (p > 14):
                    score -= min(3 / beta , 3)
            
            # Collect median prices at intervals
            
            meds.append(current_price)
            
        Price = 0
        PriceChangeMonth = 1
        
        currentPrice = daily_prices.loc[(total-1), 'Price']
        if Months == 1  and total > 1:
            PriceChangeMonth = round((1 - (daily_prices.loc[0, 'Price'] / currentPrice)) * 100,2)
        else:
            if (total > 1):
                PriceChangeMonth = round((1 - (daily_prices.loc[(int(total / 2)), 'Price'] / currentPrice)) * 100,2)
            

        PriceChangeFromHigh52 = round(1 - (currentPrice / fifty_two_week_high), 2)
        PriceChangeFromHigh52 *= 100
        # print(Stock , "Price change: " + str(PriceChangeFromHigh52 * 100))
        if (total > 0):
            Price = round(daily_prices.loc[total-1, 'Price'],2)
        # Calculate percentage change from collected medians
        perk = calculate_percent_changes(meds) if len(meds) >= 1 else 0

        # Retrieve earnings data
        eps, surprise = StockEarnings(ticker)
        averageVolume = hist['Volume'].mean()
      
        averageVolumeString = convert_to_readable(int(averageVolume))
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
        
        MyEstimate = buytime.analyze_ticker(ticker,data= hist)
        # print(MyEstimate)
        # print(Stock , Price)
        # Return computed values
        priceEstmate = 0.1
        targetHigh = .1
        score = math.ceil(score)
        if 'targetMeanPrice' in ticker.info and 'targetHighPrice' in ticker.info:
            priceEstmate = round((ticker.info.get('targetMeanPrice') +  ticker.info.get('targetHighPrice'))/ 2,2)
            targetHigh = ticker.info.get('targetHighPrice')
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
            PriceChangeMonth , PriceChangeFromHigh52  , priceEstmate , targetHigh , MyEstimate , averageVolumeString , sector , industry , 
            beta
        )
    except HTTPError as e:
            if e.response.status_code == 429:  # Too many requests
                print("Rate limit hit. Retrying...")
                time.sleep(10)

    except Exception as e:
        print('ERROR HERE')
        pass

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
        (consistency_score, avg_price_change, med_price_change, scores_mids, Sore, Eps, Surprise , price , recommendations , weeksHL , PriceChangeMonth , PriceChangeFromHigh52 , priceEstmate , targetHigh , MyEstimate , averageVolume , sector , industry , beta ) = gotcha
        
        
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
            'PriceChangeFromHigh52' : PriceChangeFromHigh52  , 
            'priceEstmate' : priceEstmate , 'targetHigh' : targetHigh , 'MyEstimate' : MyEstimate , 
            'averageVolume' : averageVolume  , 'sector' : sector , 'industry' : industry , 'beta' : beta
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
        priceEstmate = 1
        if (months != 1):
            priceEstmate = min( data['targetHigh'] / data['Price'] , 2.6)
           
            print(n , priceEstmate)
       
        # print(WeightMid , WeightAvg , WeightIncr , WeightConsis , WeightEps , WeightSurp)
        # if WeightMid > 0:
        #     # Scores[n] = round((WeightMid * 1.2) + (WeightAvg * 0.68) + (WeightIncr * 1.8) + WeightConsis + (WeightAvgMonthrise * 1.5) + priceEstmate, 2)1
        #     Scores[n] = round((WeightMid * 1.7) + (WeightAvg * 0.68) + (WeightIncr * 1.6) + WeightConsis + (WeightEps * 1.2) + (WeightSurp * 1)  + priceEstmate , 2)
        # else:
        #     print(n , "LOW EPS")
            # Scores[n] = round((WeightMid * 1.7) + (WeightAvg * 0.68) + (WeightIncr * 1.6) + WeightConsis + (WeightEps * 1.2) + (WeightSurp * 1.2) + priceEstmate + (WeightAvgMonthrise * 0.6) , 2)
        
        if (data['Price'] > 0.01):
            Scores[n] = round((WeightMid * 1.7) + (WeightAvg * 0.68) + (WeightIncr * 1.6) + WeightConsis + priceEstmate + (WeightAvgMonthrise * 0.6) , 2)
    return sorted(Scores.items(), key=lambda item: item[1]) , StoreData


# # Example usage
# value = 0
# for n in range(1,5000):
#     sorted_scores = calculate_weighted_scores(['RDDT' , 'PLTR' , 'QUBT'], months, value=n+4 , timer=True)
#     # print(sorted_scores)
#     print(n)
# ticket_symbols = [
#    'FNMA'  , 'RGTI' , 'AAL' , 'SUPV' , 'RCAT' , 'UAL' , 'ALLT'
# ]

# sorted_scores = calculate_weighted_scores(ticket_symbols, 3)
# print(sorted_scores)

def WriteToFileAverage(stock_symbols , file_path,timers=False , months=3):
        
        sorted_dict , StoreData = calculate_weighted_scores(stock_symbols , months , timer=timers)
        # print(StoreData)
        # print("Dicted")
        # print(sorted_dict)
        print("Writing to File")
        with open(file_path, "w") as file:
            for key, value in sorted_dict:
                print(key)
                # Name, Score,Price, Median, Average, Sore, Eps, Surprise, Growth Rate , Rec   , 52WeekLowHigh , PriceChangeMonth , PriceChangeFromHigh52 , targetHigh , MyEstimate rec , averageVolume
                file.write(
                    f"{key},{value},{StoreData[key]['Price']},{StoreData[key]['Mid']},"
                    f"{StoreData[key]['Avg']},{StoreData[key]['Sore']},{StoreData[key]['Eps']},{StoreData[key]['Surprise']},{StoreData[key]['Growth Rate']},{StoreData[key]['recommendation']},{StoreData[key]['52WeekLowHigh']},{StoreData[key]['PriceChangeMonth']},{StoreData[key]['PriceChangeFromHigh52']},{StoreData[key]['targetHigh']},{StoreData[key]['priceEstmate']},{StoreData[key]['MyEstimate']},{StoreData[key]['averageVolume']},"
                    f"{StoreData[key]['sector']},{StoreData[key]['industry']},{StoreData[key]['beta']}\n"
                    )
        
# WriteToFileAverage(['QUBT' , 'PLTR'] , "out.txt")
 # Function to fetch proxies from the API

# Replace 'AAPL' with your desired ticker symbol
# ticker = "KOD"
# analyze_ticker(ticker)



# 1959872.73 -- bbai
# 2156477.27 - pltr
# 3251318.18 - ACHR
# 2156477.27 - rgti
# 1094595.45 - QBTS
# 805127.27 - QUBT
# 547104.55 RKLB

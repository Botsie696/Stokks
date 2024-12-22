import yfinance as yf
import requests
import re
import openai
from datetime import datetime ,timedelta

import os
# URL of Yahoo Finance Day Gainers page
url1 = 'https://finance.yahoo.com/screener/predefined/day_gainers/'
url8 = 'https://finance.yahoo.com/research-hub/screener/day_gainers/'
url2 = 'https://finance.yahoo.com/screener/predefined/growth_technology_stocks/'
url3 = 'https://finance.yahoo.com/screener/predefined/aggressive_small_caps/'
url4 = 'https://finance.yahoo.com/markets/stocks/most-active/'
url5 =  'https://finance.yahoo.com/research-hub/screener/most_actives/'
url6 = 'https://finance.yahoo.com/markets/stocks/52-week-gainers/'
url7 = 'https://finance.yahoo.com/markets/stocks/trending/'
openai.api_key = os.getenv("OPENAI_API_KEY")

def GetStock(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    # with open("Trial.txt", "w") as file:
    #     file.write(str(response.content))
    if response.status_code == 200:
        try:
            # Extract both 'symbol' and 'data-symbol' attributes
            data_symbols = re.findall(r'data-symbol="(.*?)"', response.text)
            symbols = re.findall(r'"symbol":"(.*?)"', response.text)
            
            # Combine and deduplicate
            all_symbols = data_symbols + symbols
            seen = set()
            unique_symbols = [x for x in all_symbols if not (x in seen or seen.add(x))]
            return unique_symbols
        except Exception as e:
            print(f"Error parsing symbols: {e}")
    else:
        print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
    return []

def GatherStocks():
    stock_symbols = []
    # stock_symbols = ['RDDT' , 'QUBT' , 'PLTR' , 'TSLA' ]
    urlsHub = [url1 , url2 , url3 , url4 , url5 , url6 , url7 ]
    for n in urlsHub:
        stock_symbols += GetStock(n)
    
    stock_symbols += ['TSSI', 'WGS', 'RCAT', 'APP', 'KINS', 'AENT', 'WLFC', 'CANG', 'BYRN', 'RKLB', 'SUPV', 'RDW', 'RDDT', 'ETON', 'PLTR', 'RGTI', 'QUBT', 'EXOD', 'EAT', 'NN', 'EUDA', 'DAVE', 'CRDO', 'CLS', 'BMA', 'ALLT', 'REAL', 'GGAL', 'MTEK', 'VST', 'BBAR', 'WAVE', 'LFVN', 'MESO', 'AGX', 'PDEX', 'ICLK', 'LUNR', 'CVNA', 'RAIL', 'TLN', 'MSTR', 'UI', 'SEI', 'SMTC', 'DSP', 'BKTI', 'IPX', 'ADMA', 'HOOD', 'SMWB', 'PPTA', 'QFIN', 'IONQ', 'TATT', 'SE', 'GEV', 'EDN', 'OXBR', 'TPC', 'INSG', 'SOUN', 'DOGZ', 'PL', 'YPF', 'PRM', 'ARQT', 'CMPO', 'ECOR', 'TECX', 'USLM', 'TARS', 'SFM', 'INOD', 'RZLT', 'CLBT', 'ZETA', 'CRVS', 'UAL', 'DDL', 'SMR', 'JVA', 'RSI', 'TPB', 'FTAI', 'VRNA', 'QTWO', 'ELMD', 'PRTH', 'NTRA', 'PRAX', 'KOD', 'COMM', 'AVPT', 'APEI', 'CAVA', 'EOSE', 'SPOT', 'FLXS', 'NVDA']

    stock_symbols = list(set(stock_symbols))
    return stock_symbols
stock_symbols = GatherStocks()


# Hot
KeyWordsHot = ["Phase" , "Positive" , "Top Line" , "Top-Line" , "Significant" , "Demonstrates" , "Treatment" , "Drug Trial" , "Drug Trials" , "Agreement" , "Cancer" , "partner" , "Partnership" , "Collaboration" , "Improvment" , "success" , "Billionarie" , "Carl Ichan" , "Increase" , "Award" , "Awarded" , "Primary" , "Signs" , "Deals"]
KeyWordGood = ["Phase" , "FDA" , "Approval" , "Beneficial" , "Fast Track" , "Breaout" , "Acquisition" , "Expand" , "Expansion" , "Contract" , "Completes" , "Promising" , "Achieve" , "Launches" , "Merger" , "Gain" , "beat" , "Buy rating" , "strong buy" , "outperform", "Price target raised" , "raised"]
KeyWordsHot += KeyWordGood
KeyWordsHot = [item.lower() for item in KeyWordsHot]
 


def find_keys_with_partial_match(data_dict, match_array):
    matching_keys = []

    # Compile regex patterns for the match array
    patterns = [re.compile(rf"\b{re.escape(word)}", re.IGNORECASE) for word in match_array]

    for key, value in data_dict.items():
        value_lower = value.lower()  # Convert value to lowercase for consistent matching

        # Check for matches in the match array
        for pattern in patterns:
            if pattern.search(value_lower):
                # print(f"Matched: {value}")
                matching_keys.append(key)
                break  # No need to check further once matched

    if not matching_keys:
        print("No match found.")
    return matching_keys


def get_latest_news(ticker):
    stock = yf.Ticker(ticker)
    news = stock.news
    # print(str(news))
    return news
StocksNews = {}
# stock_symbols = ['QUBT' , 'META' , 'RDDT' , "AAPL"]
print(stock_symbols)
def GetNews():
    for n in stock_symbols:
        try:
            ticker = n # Replace with your desired stock ticker
            latest_news = get_latest_news(ticker)
            totals = ""
            # print(latest_news)
            i = 0
            print(n)
            for article in latest_news:
                if (i > 1):
                    break
                publish_time = datetime.utcfromtimestamp(article['providerPublishTime'])
                current_date = datetime.utcnow().date()
                yesterday_date = current_date - timedelta(days=1)
                print(f"Title: {article['title']}")
                print(f"Published: {publish_time}")
                # Determine if the article is published today, yesterday, or earlier
                if publish_time.date() == current_date or publish_time.date() == yesterday_date:
                    day_info = "Today"
                    totals += article['title'] + " "
                
                
                print(f"Title: {article['title']}")
                
               
        except Exception as e:
            pass
            # print(article["title"])
            i += 1
        print("Done--")
        StocksNews[n] = totals
        # print(n + ":" + totals)
    keys = find_keys_with_partial_match(StocksNews , KeyWordsHot )
    print(keys)
    stocker = {}
    for n in keys:
        stocker[n] = StocksNews[n]
    return stocker
    
# ['INSG', 'WLFC', 'LUMN', 'KINS', 'NTRA', 'CRDO', '^DJI', 'NN', 'SUPV', 'KO', 'NOW', 'DJT', 'RKLB', 'PG', 'GEV', 'GGAL', 'MTEK', 'TSSI', 'PRAX', 'ZETA', 'ASTS', 'BYRN', 'MESO', 'ARQT', 'CANG', 'WBD', 'RSI', 'EUDA', 'DSP', 'HOOD', 'INOD', 'RNA', 'MMM', 'TECX', 'VTRS', 'ICLK', 'IPX', 'PL', 'RZLT', 'COMM', 'PLTR', 'QTWO', 'HIMS', 'PRM', 'DIS', 'ACHR', 'KOD', 'MSTR', 'RAIL', 'CMPO', 'REAL', 'YPF', 'CVX', 'RXRX', 'IBM', 'RDW', 'PHIO', 'AENT', 'SIDU', 'KC', 'SBUX', 'SPOT', 'RDDT', 'TARS', 'MPW', 'TSLA', 'SOFI', 'JVA', 'PLUG', 'GOOGL', 'EOSE', 'WGS', 'ECOR', 'TLN', 'UAL', 'CRVS', 'AVPT', 'ETON', 'APP', '^GSPC', 'NVO', 'PPTA']
stocker = GetNews()

prompt = (
            "Based on the following which stock will rise the highest based on their recent news, which is the highest, given array in descending order from most rise to least rise:\n\n"
            f"{stocker} give reason why the stock will rise based on the reasons and make sure to split each stock with next line gap"
        )
# return in array like format with stock ticker symbols only, no other words, sentence, or explanation. example [AAPL,META]

# return in array like format with stock ticker symbols only, no other words, sentence, or explanation example [AAPL,META]
def ask_chatgpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a financial analyst."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error communicating with ChatGPT: {e}")
        return None

ecommendations = ask_chatgpt(prompt)
stock_symbols = ecommendations.strip("[]").split(",")
cleaned_list = [item.strip('"').strip("'") for item in stock_symbols]
for n in stock_symbols:
    print(n)
print(stock_symbols)

file_name = "News-Report.txt"
with open(file_name, 'w') as file:
    file.write(str(ecommendations))

# Percentage its rissen today in one day - optional

# file_path = "NewsTime.txt"
# betterstokks.WriteToFileAverage(stock_symbols , file_path)
# import read
# read.StoreData("NewsTime.csv" , file_path)

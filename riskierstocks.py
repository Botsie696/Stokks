from youtube_search import YoutubeSearch
import pprint
import openai
import os
from datetime import datetime, timedelta
# 
import requests
import re
openai.api_key = os.getenv("OPENAI_API_KEY")

import betterstokks

class StokksData:

    def __init__(self):
        YoutubeTitles = self.GetTitles()
        prompt = (
            "from the given list, Return all the stock Ticker symbols mentioned in the strings below, return in an array format only - FORMAT SHOULD BE THIS WAY ONLY, no other texts,  this format only give one array , Make sure to get all the stocks mentioned in these transcript, double check on them, give data like:  [NDAQ,APPLE,x,Y,Z] "
            f"{YoutubeTitles}"
        )
        Title = self.ask_chatgpt(prompt)
        listStocks = self.clean_and_extract(Title)
        print(listStocks)
        stock_symbols = self.GatherStocks() + listStocks
        stock_symbols = list(set(stock_symbols))
        print(stock_symbols , len(stock_symbols))
        
        file_path = "Risky.txt"
        betterstokks.WriteToFileAverage(stock_symbols , file_path , months=1)
        import read
        read.StoreData("Risky.csv" , file_path)



    def clean_and_extract(self , data):
        # Remove unwanted characters like `, ', and "
        clean_data = re.sub(r"[`'\"*]", "", data)

        # Extract the array content
        if clean_data.startswith("[") and clean_data.endswith("]"):
            clean_data = clean_data[1:-1]

        # Split into a list
        return [item.strip() for item in clean_data.split(",")]

    def ask_chatgpt(self , prompt):
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
    def is_recent_upload(self , published_time):
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        
        published_time = str(published_time)
        # Adjust for string matching based on the format returned by YoutubeSearch
        if "ago" in published_time:
            if  ("1 day" in published_time or "hours" in published_time or '0' in published_time or '2 days' in published_time):
                return True
            elif "hour" in published_time or "minute" in published_time:
                return True
        return False

    
    def GetTitles(self):
        youtubers = ["mr. sicko Trading", "UndeRadar Talks"]
        YoutubeTitleStocks = []
        for n in youtubers:
            Stocks = YoutubeSearch(('Recently uploaded: stocks with ' + n), max_results=(5000)).to_dict()
            BestStocks = []
            
            # pprint.pprint(Stocks)
            for video in Stocks:
                # print(video['title'])
              
                if self.is_recent_upload(video.get('publish_time', '')) and n.lower() in video.get('channel').lower():
                    # print(video['title'])
                    # Link = 'https://www.youtube.com' + video['url_suffix']
                    BestStocks.append(video['title'])
                
            YoutubeTitleStocks += BestStocks
        return YoutubeTitleStocks


    def GetStock(self, url):
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

    def GatherStocks(self):
                # URL of Yahoo Finance Day Gainers page
        url1 = 'https://finance.yahoo.com/screener/predefined/day_gainers/'
        url8 = 'https://finance.yahoo.com/research-hub/screener/day_gainers/'
        url2 = 'https://finance.yahoo.com/screener/predefined/growth_technology_stocks/'
        url3 = 'https://finance.yahoo.com/screener/predefined/aggressive_small_caps/'
        url4 = 'https://finance.yahoo.com/markets/stocks/most-active/'
        url5 =  'https://finance.yahoo.com/research-hub/screener/most_actives/'
        url6 = 'https://finance.yahoo.com/markets/stocks/52-week-gainers/'
        url7 = 'https://finance.yahoo.com/markets/stocks/trending/'


        stock_symbols = []
        # stock_symbols = ['RDDT' , 'QUBT' , 'PLTR' , 'TSLA' ]
        urlsHub = [url1 , url2 , url3 , url4 , url5 , url6 , url7 ]
        for n in urlsHub:
            stock_symbols += self.GetStock(n)
        
        stock_symbols += ['TSSI', 'WGS', 'RCAT', 'APP', 'KINS', 'AENT', 'WLFC', 'CANG', 'BYRN', 'RKLB', 'SUPV', 'RDW', 'RDDT', 'ETON', 'PLTR', 'RGTI', 'QUBT', 'EXOD', 'EAT', 'NN', 'EUDA', 'DAVE', 'CRDO', 'CLS', 'BMA', 'ALLT', 'REAL', 'GGAL', 'MTEK', 'VST', 'BBAR', 'WAVE', 'LFVN', 'MESO', 'AGX', 'PDEX', 'ICLK', 'LUNR', 'CVNA', 'RAIL', 'TLN', 'MSTR', 'UI', 'SEI', 'SMTC', 'DSP', 'BKTI', 'IPX', 'ADMA', 'HOOD', 'SMWB', 'PPTA', 'QFIN', 'IONQ', 'TATT', 'SE', 'GEV', 'EDN', 'OXBR', 'TPC', 'INSG', 'SOUN', 'DOGZ', 'PL', 'YPF', 'PRM', 'ARQT', 'CMPO', 'ECOR', 'TECX', 'USLM', 'TARS', 'SFM', 'INOD', 'RZLT', 'CLBT', 'ZETA', 'CRVS', 'UAL', 'DDL', 'SMR', 'JVA', 'RSI', 'TPB', 'FTAI', 'VRNA', 'QTWO', 'ELMD', 'PRTH', 'NTRA', 'PRAX', 'KOD', 'COMM', 'AVPT', 'APEI', 'CAVA', 'EOSE', 'SPOT', 'FLXS', 'NVDA']

        stock_symbols = list(set(stock_symbols))
        return stock_symbols

Data = StokksData()
# YoutubeTitleStocks = StokksData.GetTitles()
# print(YoutubeTitleStocks)
import requests
import financedata
import dataprovider
from lxml import html
import re
import betterstokks
# Add price targets
def safe_convert(value):
    try:
        return float(value)  # Try to convert to float
    except ValueError:
        return 0.0  # Return None if conversion fail

# URL of Yahoo Finance Day Gainers page
url1 = 'https://finance.yahoo.com/screener/predefined/day_gainers/'
url8 = 'https://finance.yahoo.com/research-hub/screener/day_gainers/'
url2 = 'https://finance.yahoo.com/screener/predefined/growth_technology_stocks/'
url3 = 'https://finance.yahoo.com/screener/predefined/aggressive_small_caps/'
url4 = 'https://finance.yahoo.com/markets/stocks/most-active/'
url5 =  'https://finance.yahoo.com/research-hub/screener/most_actives/'
url6 = 'https://finance.yahoo.com/markets/stocks/52-week-gainers/'
url7 = 'https://finance.yahoo.com/markets/stocks/trending/'


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

stock_symbols = ['RDDT' , 'QUBT' , 'PLTR' , 'TSLA' ]
stock_symbols= []
urlsHub = [url1 , url2 , url3 , url4 , url5 , url6 , url7 ]
for n in urlsHub:
    stock_symbols += GetStock(n)
 
stock_symbols += ['TSSI', 'WGS', 'RCAT', 'APP', 'KINS', 'AENT', 'WLFC', 'CANG', 'BYRN', 'RKLB', 'SUPV', 'RDW', 'RDDT', 'ETON', 'PLTR', 'RGTI', 'QUBT', 'EXOD', 'EAT', 'NN', 'EUDA', 'DAVE', 'CRDO', 'CLS', 'BMA', 'ALLT', 'REAL', 'GGAL', 'MTEK', 'VST', 'BBAR', 'WAVE', 'LFVN', 'MESO', 'AGX', 'PDEX', 'ICLK', 'LUNR', 'CVNA', 'RAIL', 'TLN', 'MSTR', 'UI', 'SEI', 'SMTC', 'DSP', 'BKTI', 'IPX', 'ADMA', 'HOOD', 'SMWB', 'PPTA', 'QFIN', 'IONQ', 'TATT', 'SE', 'GEV', 'EDN', 'OXBR', 'TPC', 'INSG', 'SOUN', 'DOGZ', 'PL', 'YPF', 'PRM', 'ARQT', 'CMPO', 'ECOR', 'TECX', 'USLM', 'TARS', 'SFM', 'INOD', 'RZLT', 'CLBT', 'ZETA', 'CRVS', 'UAL', 'DDL', 'SMR', 'JVA', 'RSI', 'TPB', 'FTAI', 'VRNA', 'QTWO', 'ELMD', 'PRTH', 'NTRA', 'PRAX', 'KOD', 'COMM', 'AVPT', 'APEI', 'CAVA', 'EOSE', 'SPOT', 'FLXS', 'NVDA']

stock_symbols = list(set(stock_symbols))

print(stock_symbols , len(stock_symbols))



Rise = {}


file_path = "YahooDirec.txt"
betterstokks.WriteToFileAverage(stock_symbols , file_path)
import read
read.StoreData("yahoo.csv" , file_path)
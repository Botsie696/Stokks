import requests
import financedata
import dataprovider
from lxml import html
import re
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

stock_symbols = []
urlsHub = [url1 , url2 , url3 , url4 , url5 , url6 , url7 , url8]
for n in urlsHub:
    stock_symbols += GetStock(n)
stock_symbols = list(set(stock_symbols))
print(stock_symbols , len(stock_symbols))

# import allstocks
# stock_symbols = allstocks.common_stock_symbols
# stock_symbols = GetStocks(url3)
# Print the extracted stock symbols
 

Rise = {}

def GetStocks(stock_symbols):
        
        StockPrice = {}
        StockRevenue = {}
        Consistency = {}
        AverageScore = {}
        MedianScore = {}
        ConsistencyScores = {}
        HighestMedianScore =0 
        HighestAverageScore = 0
        HighestConsistancyScore = 0
        HighestRiseScore = 0
        EstimatedPrice = {}
        StockRecommended = {}
        PriceRise = {}
        print("Onto setting the to the loop")
        StockFinalSyms = []
        for n in stock_symbols:
                
            # time.sleep(3)
            # print("Printing data for " + n)
            Percent, Price  , Name = financedata.AnalyseWithYahoo(n)
            if (Price == "NONE" or Price == None or Price == "NONE"):
                pass
            estimatedPrice , Recommended = financedata.GetEstimatePrice(Name)
            StockFinalSyms.append(Name)
            StockRev = financedata.GetRevenue(Name)
            ConsisStockRev , Average , Median , ScoresMids = financedata.ConsistancyScore(Name , dataprovider.Months , Distance=dataprovider.DepthForScore)
            Rise[n] = str(Percent)
            EstimatedPrice[n] = estimatedPrice
            StockRecommended[n] = Recommended
            Consistency[n] = ConsisStockRev
            ConsistencyScores[n] = ScoresMids
            AverageScore[n] = Average
            MedianScore[n] = Median
            StockPrice[n] = Price
            StockRevenue[n] = StockRev 

          
            try:
                PricePop =  1 - round((float(Price) / estimatedPrice) , 2)
                PriceRise[n] = round(PricePop , 2)
                print("Safe converting")
                if safe_convert(ScoresMids) > HighestConsistancyScore:
                    HighestConsistancyScore = ScoresMids
                if safe_convert(Average)> HighestAverageScore:
                    HighestAverageScore = Average
                if safe_convert(Median) > HighestMedianScore:
                    HighestMedianScore = Median
                
                if safe_convert(Percent) > HighestRiseScore:
                    HighestRiseScore = Percent
            except Exception as e:
                print("error but go" )
                continue
            


        
       

        # Filter and convert values to numbers
        filtered_dict = {k: safe_convert(v) for k, v in Rise.items() if safe_convert(v) is not None}

        # Sort the dictionary by value
        sorted_dict = dict(sorted(filtered_dict.items(), key=lambda item: item[1]))

        # Write to a text file
        file_path = "YahooDirec.txt"
        # print("Dicted")
        # print(sorted_dict)
        print("Writing to File")
        with open(file_path, "w") as file:
            for key, value in sorted_dict.items():
               ScoresPuts =0
               try:
                    print(MedianScore)
                    print(key)
                    Meds = (MedianScore[key] / HighestMedianScore)
                    Avgs = (AverageScore[key] / HighestAverageScore)
                    vals = (value / HighestRiseScore)
                    consis = (ConsistencyScores[key] / HighestConsistancyScore)
                    
                    ScoresPuts = round((Meds + Avgs + vals + consis) , 2)
               except TypeError:
                   print("Type error")
                   pass
            
               
               if key in StockRevenue and key in PriceRise:  
                    print("Adding file")
                    file.write(
                            f"{key},{value},{StockPrice[key]},{StockRevenue[key]},"
                            f"{Consistency[key]},{AverageScore[key]},{MedianScore[key]},{ScoresPuts},{EstimatedPrice[key]},{StockRecommended[key]},{PriceRise[key]}\n"
                            )
        import read
        read.StoreData("yahoo.csv" , file_path)
        

GetStocks(stock_symbols)
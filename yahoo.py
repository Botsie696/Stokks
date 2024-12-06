import requests
import financedata
import dataprovider
from lxml import html
 
def safe_convert(value):
    try:
        return float(value)  # Try to convert to float
    except ValueError:
        return 0.0  # Return None if conversion fail

# URL of Yahoo Finance Day Gainers page
url = 'https://finance.yahoo.com/screener/predefined/day_gainers/'
url2 = 'https://finance.yahoo.com/screener/predefined/growth_technology_stocks/'

def GetStocks(url):
# Set headers to mimic a browser visit
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Fetch the page content
    response = requests.get(url, headers=headers)
    # Parse the HTML content
    tree = html.fromstring(response.content)
    # Extract stock symbols using XPath
    stock_symbols = tree.xpath('//a[@data-test="quoteLink"]/text()')
    return stock_symbols

stock_symbols = GetStocks(url)
stock_symbols2 = GetStocks(url2)

stock_symbols += stock_symbols2

# Print the extracted stock symbols
for symbol in stock_symbols:
    print(symbol)


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
        print("Onto setting the to the loop")
        StockFinalSyms = []
        for n in stock_symbols:
            # print("Printing data for " + n)
            Percent, Price  , Name = financedata.AnalyseWithYahoo(n)
            if (Price == "NONE" or Price == None or Price == "NONE"):
                pass
            StockFinalSyms.append(Name)
            StockRev = financedata.GetRevenue(Name)
            ConsisStockRev , Average , Median , ScoresMids = financedata.ConsistancyScore(Name , dataprovider.Months , Distance=dataprovider.DepthForScore)
            Rise[n] = str(Percent)
            Consistency[n] = ConsisStockRev
            ConsistencyScores[n] = ScoresMids
            AverageScore[n] = Average
            MedianScore[n] = Median
            StockPrice[n] = Price
            StockRevenue[n] = StockRev 
            
            print("Safe converting")
            try:
                if safe_convert(ScoresMids) > HighestConsistancyScore:
                    HighestConsistancyScore = ScoresMids
                if safe_convert(Average)> HighestAverageScore:
                    HighestAverageScore = Average
                if safe_convert(Median) > HighestMedianScore:
                    HighestMedianScore = Median
                
                if safe_convert(Percent) > HighestRiseScore:
                    HighestRiseScore = Percent
            except Exception as e:
                print("error but go" + e)
            

        for key, value in Rise.items():
            print(f"{key}: {value}")
        # print(Rise)
        
       

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
                   pass
                   
               
               
               file.write(
                    f"{key},{value},{StockPrice[key]},{StockRevenue[key]},"
                    f"{Consistency[key]},{AverageScore[key]},{MedianScore[key]},{ScoresPuts}\n"
                    )
        import read
        read.StoreData("yahoo.csv" , file_path)
        

GetStocks(stock_symbols)
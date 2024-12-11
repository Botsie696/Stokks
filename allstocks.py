def filter_common_stock_symbols(file_path, nse_file_path):
    # List to store the stock symbols
    common_stock_symbols = []
    nse_symbols = []
    
    # Process the NASDAQ-listed file
    with open(file_path, 'r') as file:
        # Read the header
        file.readline()  # Skip the header row
        
        # Process each row
        for line in file:
            # Split the line into columns based on "|"
            columns = line.strip().split('|')
            
            # Check if "Common Stock" is in the Security Name column
            if "Common Stock" in columns[1]:  # Assuming Security Name is the second column
                # Append the stock symbol (first column) to the list
                common_stock_symbols.append(columns[0])
    
    # Process the NSE-listed CSV file
    with open(nse_file_path, 'r') as nse_file:
        # Read the header
        nse_file.readline()  # Skip the header row
        
        # Process each row
        for line in nse_file:
            # Split the line into columns based on "," (for CSV format)
            columns = line.strip().split(',')
            
            # Append the ATC Symbol (first column) to the list
            nse_symbols.append(columns[0])
    
    # Return both lists
    return common_stock_symbols, nse_symbols

# File paths to your files
nasdaq_file_path = "nasdaqlisted.txt"  # Replace with your actual file path
nse_file_path = "nyse-listed.csv"  # Replace with your actual file path

# Get data from both files
common_stock_symbols, nse_symbols = filter_common_stock_symbols(nasdaq_file_path, nse_file_path)
common_stock_symbols += nse_symbols
# Print results
print("Number of Common Stock symbols:", len(common_stock_symbols))
print("Number of ATC symbols:", len(nse_symbols))

 

import requests
import financedata
import dataprovider
from lxml import html
import time
def safe_convert(value):
    try:
        return float(value)  # Try to convert to float
    except ValueError:
        return 0.0  # Return None if conversion fail



stock_symbols = common_stock_symbols
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
        q = 0
        for n in stock_symbols:
                
            time.sleep(1)
            if (q % 30 == 0):
                print("Stock: " , n)
            q += 1
            # print("Printing data for " + n)
            Percent, Price  , Name = financedata.AnalyseWithYahoo(n)
            if (Price == "NONE" or Price == None or Price == "NONE"):
                pass
            estimatedPrice , Recommended = financedata.GetEstimatePrice(Name)
            StockFinalSyms.append(Name)
            StockRev = financedata.GetRevenue(Name)
            ConsisStockRev , Average , Median , ScoresMids = financedata.ConsistancyScore(Name , 4, Distance=8)
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
        file_path = "AllStocksWorking.txt"
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
                   
               
               if key in StockRevenue and key in PriceRise:  
                    file.write(
                            f"{key},{value},{StockPrice[key]},{StockRevenue[key]},"
                            f"{Consistency[key]},{AverageScore[key]},{MedianScore[key]},{ScoresPuts},{EstimatedPrice[key]},{StockRecommended[key]},{PriceRise[key]}\n"
                            )
        import read
        read.StoreData("newyahoo.csv" , file_path)
        

GetStocks(stock_symbols)
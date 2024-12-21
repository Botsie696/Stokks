import betterstokks
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
 
stock_symbols = list(set(stock_symbols))
print(stock_symbols)
Rise = {}

def GetStocks(stock_symbols):
        
        file_path = "AllStocksWorking.txt"
        betterstokks.WriteToFileAverage(stock_symbols , file_path)
        import read
        read.StoreData("newyahoo.csv" , file_path)
        
# GetStocks(['QUBT'])
GetStocks(stock_symbols)

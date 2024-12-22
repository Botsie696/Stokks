
import financedata
import dataprovider
def safe_convert(value):
    try:
        return float(value)  # Try to convert to float
    except ValueError:
        return 0.0  # Return None if conversion fail

# Replace with your OpenAI
def GetFileData():
    file_path = "StockList.txt"
    # Read the existing data from the file and split it into a set of unique values
    with open(file_path, "r") as file:
        existing_data = file.read().strip()
        # Strip each value of extra spaces or newlines
        existing_values = {value.strip() for value in existing_data.split(",")} if existing_data else set()
        return existing_values
    return []

import betterstokks
Rise = {}
def GetStocks(stock_symbols):
        file_path = "OldData.txt"
        betterstokks.WriteToFileAverage(stock_symbols , file_path, timers=True)
        import read
        

stockToLook = GetFileData()
print(stockToLook)
GetStocks(stockToLook)
import read
read.StoreData("outputnew.csv" , "OldData.txt" )
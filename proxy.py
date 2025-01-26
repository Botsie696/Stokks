
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
def GetStocks(stock_symbols  , file , month):
        file_path = file
        betterstokks.WriteToFileAverage(stock_symbols , file_path, timers=True , months=month)
        
        

stockToLook = GetFileData()
stockToLook = list(set(stockToLook))
# print(stockToLook)
GetStocks(stockToLook , "OldData.txt" , 3)
import read
read.StoreData("outputnew.csv" , "OldData.txt" )


GetStocks(stockToLook , "OldData1month.txt" , 1)
read.StoreData("outputnew1month.csv" , "OldData1month.txt" )
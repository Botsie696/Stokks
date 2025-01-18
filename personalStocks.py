import yfinance as yf
import betterstokks
stocks = ["AAL", "TSLA", "YPF", "NVDA", "SOFI", "ALLT", "KMDA", "BBAI", "LAES", "VRME", "RR" , 'PLTR' , 'SOUN' ]
stocks += ["GRRR", "TARS" , "RCAT" , "SPCB" , "SUPV"]

file_path = "PersonalStocks.txt"
betterstokks.WriteToFileAverage(stocks , file_path   ,  months=1)
import read
read.StoreData("PersonalStocks.csv" , file_path )

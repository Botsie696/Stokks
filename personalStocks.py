import yfinance as yf
import betterstokks
stocks = ["AAL", "TSLA", "NVDA", "SOFI", "ALLT", "KMDA", "BBAI",  "VRME", "RR" , 'PLTR' , 'SOUN' ]
stocks += ["GRRR", "TARS" , "RCAT" , "SPCB" , "SUPV" , "ACHR" , "LUNR" , "LBRT" , "SWMB" , "HUT" , "KTOS" , "CRK" , "SEI" , "WULF"]

file_path = "PersonalStocks.txt"
betterstokks.WriteToFileAverage(stocks , file_path   ,  months=3)
import read
read.StoreData("PersonalStocks.csv" , file_path )

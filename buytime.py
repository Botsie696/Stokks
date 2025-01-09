import yfinance as yf
import pandas as pd
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def analyze_ticker(ticker , data=None):
    # Download data for the past 1 month with daily intervals
    # data = yf.download(ticker, period="1mo", interval="5d")
    
    if (data is None):
        data = yf.download(ticker, period="1mo", interval="5d")
    # data = yf.download(ticker, period="1d", interval="15m")

   
    if data.empty:
        print(f"No data available for ticker {ticker}")
        return
    
    # Calculate daily price change percentage
    data['Price Change %'] = data['Close'].pct_change() * 100
    # Classify as "Buy" if price increased and "Sell" if price decreased
    data['Buy/Sell Estimate'] = data['Price Change %'].apply(lambda x: "Buy" if x > 0 else "Sell")
    data['Volume Change'] = data['Volume'].diff()
    data['Volume Pct'] = data['Volume'].pct_change()
     
    # Adjust classifications based on specific conditions
    buyers = 0
    datalower = []
    for i in range(1, len(data) ):
         
        if (data['Price Change %'].iloc[i] > 0):
            volumes =  int(data['Volume'].iloc[i] - (data['Volume'].iloc[i]/(2 + (data['Price Change %'].iloc[i]/100))))
            datalower.append(volumes)    
            buyers += int(volumes)
            # print(volumes ,"+"  , buyers , "===>" , data['Volume'].iloc[i])
             
        else:
            volumes =   (data['Volume'].iloc[i]/(2 + abs(data['Price Change %'].iloc[i]/100)))
            
            buyers -= int(volumes)
            # print( "==", abs(data['Price Change %'].iloc[i]/100) , volumes  , "-" , buyers , "==>" , data['Volume'].iloc[i])
            datalower.append(-volumes)    
        
        

        dataPct = data['Volume'].iloc[i] /  data['Volume'].iloc[i-1]
        

        if (data['Buy/Sell Estimate'].iloc[i] == "Sell" and data['Volume Change'].iloc[i] > 0 and
            (data['Price Change %'].iloc[i] < -1.2 and 
            float(dataPct) > 1.20 ) or (data['Price Change %'].iloc[i] < -4 and   float(dataPct) > 1.35 )):
            data.loc[data.index[i], 'Buy/Sell Estimate'] = "Sell ALL"
        if (data['Buy/Sell Estimate'].iloc[i] == "Sell" and data['Volume Change'].iloc[i] > 0):
            data.loc[data.index[i], 'Buy/Sell Estimate'] = "Sell ALL"

       
        if (data['Buy/Sell Estimate'].iloc[i] == "Sell ALL" and (data['Volume Pct'].iloc[i] ) < .15):
            data.loc[data.index[i], 'Buy/Sell Estimate'] = "== less Sell ALL=="

        if (data['Buy/Sell Estimate'].iloc[i] == "Buy"
             and data['Volume Change'].iloc[i] > 0 and 
             "Buy" in data['Buy/Sell Estimate'].iloc[i-1]):
            data.loc[data.index[i], 'Buy/Sell Estimate'] = "Buy time"

        # == Sell
        if ("Sell" not in data['Buy/Sell Estimate'].iloc[i-1] and 
            float(dataPct) < .54 and
            "mere" not in data['Buy/Sell Estimate'].iloc[i-1] and 
            data['Buy/Sell Estimate'].iloc[i] == "Sell" and data['Volume Change'].iloc[i] < 0):
            data.loc[data.index[i], 'Buy/Sell Estimate'] = "mere Buy (some sold)"

        # == Sell
        if ("Buy" not in data['Buy/Sell Estimate'].iloc[i-1] and 
            float(dataPct) > .55 and
            "mere" not in data['Buy/Sell Estimate'].iloc[i-1] and 
            data['Buy/Sell Estimate'].iloc[i] == "Sell" and data['Volume Change'].iloc[i] < 0):
            data.loc[data.index[i], 'Buy/Sell Estimate'] = "mere Sell (some bought)"

        # == Buy
        if ("Buy" not in data['Buy/Sell Estimate'].iloc[i-1] and 
            (float(dataPct)) > 1.25 and
            "mere" not in data['Buy/Sell Estimate'].iloc[i-1] and 
            data['Buy/Sell Estimate'].iloc[i] == "Buy" and (data['Volume Change'].iloc[i] > 0 )):
            data.loc[data.index[i], 'Buy/Sell Estimate'] = "- Buy time -"

        if ("Buy" in data['Buy/Sell Estimate'].iloc[i-1] and 
            (float(dataPct)) > .64 and
            data['Buy/Sell Estimate'].iloc[i] == "Buy"):
            data.loc[data.index[i], 'Buy/Sell Estimate'] = "- +Buy time -"

        # print(float(dataPct))


    # Calculate the count of "Buy" and "Sell"
    # buy_count = (data['Buy/Sell Estimate'] == "Buy").sum() + (data['Buy/Sell Estimate'] == "Buy time").sum()
    # sell_count = (data['Buy/Sell Estimate'] == "Sell").sum() + (data['Buy/Sell Estimate'] == "Sell ALL").sum()
    # buy_countTime = (data['Buy/Sell Estimate'] == "Buy time").sum()
    # Calculate the mean of the volume change
    # mean_volume_change = data['Volume'].mean()
    # print(mean_volume_change)
    # # Summarize data
    # print("Analyzed Data for the Past Month:\n")
    # print(data[['Open', 'Close', 'Volume', 'Price Change %', 'Buy/Sell Estimate', 'Volume Change'  , 'Volume Pct']])
    # print("\nSummary:")
    # print(f"Total 'Buy' instances: {buy_countTime}")
    # print(f"Total 'Sell' instances: {sell_count}")
    # print(f"\nMean of Volume Change: {mean_volume_change}")
    # print("Volume change" , data['Volume'].pct_change().mean())
    # print(buyers  , "Buyer with " , int(sum(datalower) / len(datalower) )   )
    # if buy_count > sell_count:
    #     print(f"Overall BUY by {buy_countTime}")
    # else:
    #     print(f"Overall SELL by {buy_countTime}")
    # print("Final Data" , f"{data['Volume Pct'].iloc[len(data) - 1]:.2}" , data['Buy/Sell Estimate'].iloc[len(data) - 1], data['Buy/Sell Estimate'].iloc[len(data) - 2])

    return f"{data['Buy/Sell Estimate'].iloc[len(data) - 1]}" 
# ticker = "SOUN"
# ticler = analyze_ticker(ticker)
# print(ticler)
# prev day has to be buy then buy time to buy 
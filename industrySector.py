import yfinance as yf
import time
import pandas as pd
# ticker = 'NNOX'
# price_target = get_price_target(ticker) 
    # Get ticker data
import requests
import re
# Define the stock ticker
ticker_symbol = "ESOA"  # Replace with your desired stock ticker

# Fetch the stock data
stock = yf.Ticker(ticker_symbol)

# Get the industry and sector information
industry = stock.info.get("industry", "Industry not available")
sector = stock.info.get("sector", "Sector not available")

stocksSP500 = [
    "AAPL", "NVDA", "MSFT", "GOOG", "GOOGL", "AMZN", "META", "TSLA", "AVGO", "BRK.B", 
    "WMT", "LLY", "JPM", "V", "UNH", "XOM", "MA", "ORCL", "COST", "HD",
    "PG", "NFLX", "BAC", "JNJ", "ABBV", "CRM", "CVX", "KO", "MRK", "TMUS", 
    "CSCO", "WFC", "ACN", "NOW", "TMO", "AXP", "IBM", "MCD", "BX", "MS", 
    "PEP", "LIN", "DIS", "ISRG", "ABT", "AMD", "GE", "GS", "PM", "ADBE", 
    "INTU", "QCOM", "TXN", "DHR", "CAT", "VZ", "BKNG", "T", "PLTR", "RTX",
    "PFE", "SPGI", "BLK", "ANET", "HON", "AMGN", "LOW", "BSX", "AMAT", "SYK",
    "CMCSA", "UBER", "NEE", "PGR", "UNP", "C", "TJX", "ETN", "SCHW", "COP",
    "BA", "KKR", "ADP", "FI", "PANW", "BMY", "GILD", "DE", "LMT", "MU",
    "VRTX", "ADI", "NKE", "UPS", "SBUX", "CB", "MDT", "MMC", "GEV", "PLD",
    "LRCX", "CEG", "KLAC", "SO", "ELV", "APO", "EQIX", "MO", "CRWD", "TT",
    "APH", "PYPL", "WM", "SHW", "CME", "INTC", "MCO", "CDNS", "ICE", "DUK",
    "PH", "AMT", "ABNB", "DELL", "WELL", "CI", "CMG", "HCA", "CTAS", "SNPS",
    "MSI", "AON", "MAR", "MDLZ", "PNC", "REGN", "USB", "EOG", "MCK", "ZTS",
    "FTNT", "ITW", "AJG", "MMM", "GD", "TDG", "CL", "ORLY", "BDX", "WMB",
    "EMR", "COF", "NOC", "WDAY", "FDX", "APD", "ECL", "TGT", "RSG", "SPG",
    "KMI", "CSX", "ADSK", "RCL", "CVS", "CARR", "OKE", "HLT", "DLR", "TFC",
    "VST", "AFL", "FCX", "PCAR", "MET", "BK", "GM", "AZO", "SLB", "ROP",
    "CPRT", "CHTR", "NSC", "TRV", "NXPI", "JCI", "GWW", "FANG", "PSA", "PAYX",
    "ROST", "AMP", "SRE", "AEP", "CMI", "MNST", "LULU", "OXY", "ALL", "PSX",
    "FICO", "PWR", "HWM", "MPC", "COR", "O", "MSCI", "D", "NEM", "URI",
    "AIG", "DHI", "HES", "NDAQ", "AXON", "EW", "DAL", "BKR", "KR", "DFS",
    "TEL", "TRGP", "PEG", "FIS", "KMB", "KDP", "FAST", "PRU", "AME", "GLW",
    "VLO", "GRMN", "KVUE", "LHX", "A", "CTVA", "GEHC", "F", "VRSK", "IT",
    "ODFL", "PCG", "EXC", "CTSH", "CBRE", "EA", "IQV", "CCI", "XEL", "OTIS",
    "SYY", "UAL", "LEN", "IR", "KHC", "YUM", "RMD", "IDXX", "LVS", "ACGL",
    "VMC", "WAB", "STZ", "ETR", "HUM", "EXR", "GIS", "HSY", "CCL", "EBAY",
    "DECK", "WTW", "RJF", "TTWO", "CNC", "MTB", "HPQ", "MLM", "ROK", "HIG",
    "ED", "DD", "DXCM", "EFX", "AVB", "TPL", "VICI", "IRM", "MCHP", "LYV",
    "WEC", "ANSS", "CAH", "EQT", "TSCO", "BRO", "HPE", "MPWR", "CSGP", "K",
    "KEYS", "NUE", "XYL", "FITB", "STT", "GDDY", "DOW", "GPN", "SW", "EL",
    "PPG", "EQR", "FTV", "BR", "MTD", "DOV", "EIX", "CHD", "SYF", "VLTO",
    "DTE", "ADM", "CDW", "CPAY", "VTR", "TROW", "NVR", "WST", "TYL", "WBD",
    "HAL", "DVN", "NTAP", "AWK", "LYB", "AEE", "PPL", "HBAN", "EXPE", "ON",
    "WAT", "HUBB", "ROL", "FE", "PHM", "FOXA", "PTC", "TER", "LII", "WDC",
    "BIIB", "WRB", "FOX", "ATO", "TDY", "CINF", "DRI", "RF", "ZBH", "IFF",
    "SBAC", "CTRA", "ES", "ERIE", "PKG", "CNP", "STE", "FSLR", "NRG", "CBOE",
    "LDOS", "VRSN", "ZBRA", "LUV", "WY", "NTRS", "CLX", "CMS", "LH", "ULTA",
    "TSN", "MKC", "SMCI", "CFG", "PODD", "STX", "IP", "INVH", "ESS", "COO",
    "BBY", "MAA", "STLD", "L", "JBHT", "PFG", "SNA", "FDS", "TRMB", "DGX",
    "NI", "JBL", "ARE", "GEN", "KEY", "HRL", "J", "MOH", "HOLX", "MRNA",
    "OMC", "GPC", "BLDR", "PNR", "BF.B", "NWS", "ALGN", "DG", "DLTR", "IEX",
    "MAS", "BALL", "CF", "TPR", "NWSA", "EXPD", "EG", "BAX", "UDR", "FFIV",
    "AVY", "RL", "KIM", "LNT", "SWKS", "TXT", "DOC", "APTV", "VTRS", "DPZ",
    "RVTY", "EVRG", "INCY", "AMCR", "AKAM", "EPAM", "JNPR", "DVA", "JKHY",
    "REG", "POOL", "CAG", "SWK", "UHS", "KMX", "CHRW", "BXP", "HST", "CPT",
    "TECH", "SOLV", "NDSN", "BG", "NCLH", "PAYC", "CPB", "DAY", "ALLE", "TAP",
    "SJM", "AIZ", "ALB", "WBA", "EMN", "BEN", "IPG", "AOS", "CRL", "MGM",
    "GL", "LKQ", "GNRC", "PNW", "ENPH", "WYNN", "APA", "FRT", "HSIC", "LW",
    "AES", "MKTX", "TFX", "HAS", "MOS", "MTCH", "MHK", "HII", "IVZ", "CE",
    "PARA", "BWA", "CZR", "FMC"
]


stock_symbols = ['TSSI', 'WGS', 'RCAT', 'APP', 'KINS', 'AENT', 'WLFC', 'CANG', 'BYRN', 'RKLB', 'SUPV', 'RDW', 'RDDT', 'ETON', 'PLTR', 'RGTI', 'QUBT', 'EXOD', 'EAT', 'NN', 'EUDA', 'DAVE', 'CRDO', 'CLS', 'BMA', 'ALLT', 'REAL', 'GGAL', 'MTEK', 'VST', 'BBAR', 'WAVE', 'LFVN', 'MESO', 'AGX', 'PDEX', 'ICLK', 'LUNR', 'CVNA', 'RAIL', 'TLN', 'MSTR', 'UI', 'SEI', 'SMTC', 'DSP', 'BKTI', 'IPX', 'ADMA', 'HOOD', 'SMWB', 'PPTA', 'QFIN', 'IONQ', 'TATT', 'SE', 'GEV', 'EDN', 'OXBR', 'TPC', 'INSG', 'SOUN', 'DOGZ', 'PL', 'YPF', 'PRM', 'ARQT', 'CMPO', 'ECOR', 'TECX', 'USLM', 'TARS', 'SFM', 'INOD', 'RZLT', 'CLBT', 'ZETA', 'CRVS', 'UAL', 'DDL', 'SMR', 'JVA', 'RSI', 'TPB', 'FTAI', 'VRNA', 'QTWO', 'ELMD', 'PRTH', 'NTRA', 'PRAX', 'KOD', 'COMM', 'AVPT', 'APEI', 'CAVA', 'EOSE', 'SPOT', 'FLXS', 'NVDA']
stock_symbols += [
"CMMB", "HTCR", "WNW", "OXBR", "BFLY", "JVA", "HTCO", "LPTH", "SLQT", "PL", 
"EUDA", "MTEK", "RZLT", "CANG", "EOSE", "NEOV", "CRVS", "ALLT", "DUOT", "QBTS", 
"REAL", "FTEL", "AENT", "RAIL", "INSG", "ICLK", "PRTH", "PRM", "ETON", "RCAT", 
"TSSI", "INLX", "RSI", "SMWB", "KINS", "CMPO", "NN", "SUPV", "ECOR", "QUBT", 
"LFVN", "RDW", "ADMA", "ZETA", "RGTI", "DSP", "MESO", "SOUN", "SMR", "LUNR", 
"CLBT", "BBAR", "GRRR", "GDS", "BTDR", "TATT", "PSIX", "RKLB", "SEI", "BYRN", 
"ELMD", "BKTI", "IPX", "QFIN", "HOOD", "YPF", "INOD", "EDN", "VRNA", "PDEX", 
"IONQ", "TECX", "TARS", "TPB", "SMTC", "LB", "GGAL", "CRDO", "WGS", "PLTR", 
"DAVE", "CLS", "SE", "BMA", "CLMB", "SFM", "EAT", "NVDA", "AGX", "FTAI", "VST", 
"RDDT", "CRS", "TLN", "WLFC", "IESC", "MSTR", "UI", "APP", "GEV"
]

stock_symbols += [
    "EVER", "EUDA", "WGS", "KINS", "RNA", "ZETA", "REAX", "FTAI", "DYN", "ADMA", 
    "ANF", "ALAR", "USAP", "FIP", "SN", "SFM", "MMYT", "CRS", "GATO", "AEYE", 
    "INLX", "NGD", "SPRY", "HMY", "AKA", "RZLT", "CURV", "CVNA", "RCAT", "HUMA", 
    "KEQU", "VST", "BYRN", "IMPP", "NVDA", "TPC", "CVLT", "SPOT", "IAG", "BLFS", 
    "CAVA", "JXN", "IESC", "TLN", "WLFC", "RYAM", "MOD", "VIRC", "PI", "AVAH", 
    "HWKN", "MAMA", "ASTS", "BMA", "CLS", "HROW", "GDDY", "DAVE", "PRM", "HBB", 
    "THC", "ERJ", "MGNX", "CDE", "NTRA", "CDNA", "PTGX", "QTWO", "PPTA", "RDNT", 
    "APEI", "ACIW", "TMDX", "FICO", "NRG", "SUPV", "CXDO", "EAT", "AIOT", "VITL", 
    "CRDL", "HNST", "AMRX", "OSCR", "CLMB", "TAYD", "QTTB", "CLOV", "REVG", "CDRO", 
    "GRND", "WING", "GGAL", "HWM", "APLT", "ASPN", "SLQT", "CREX", "DY", "PAYS"
]
url1 = 'https://finance.yahoo.com/screener/predefined/day_gainers/'
url8 = 'https://finance.yahoo.com/research-hub/screener/day_gainers/'
url2 = 'https://finance.yahoo.com/screener/predefined/growth_technology_stocks/'
url3 = 'https://finance.yahoo.com/screener/predefined/aggressive_small_caps/'
url4 = 'https://finance.yahoo.com/markets/stocks/most-active/'
url5 =  'https://finance.yahoo.com/research-hub/screener/most_actives/'
url6 = 'https://finance.yahoo.com/markets/stocks/52-week-gainers/'
url7 = 'https://finance.yahoo.com/markets/stocks/trending/'
url8 = 'https://finance.yahoo.com/research-hub/screener/most_active_penny_stocks'
url9 = 'https://finance.yahoo.com/screener/predefined/most_active_penny_stocks'
url10 = 'https://finance.yahoo.com/research-hub/screener/analyst_strong_buy_stocks/'
url11 = 'https://finance.yahoo.com/research-hub/screener/morningstar_five_star_stocks/'
url12 = 'https://finance.yahoo.com/research-hub/screener/top_stocks_owned_by_goldman_sachs/'
url13 = 'https://finance.yahoo.com/research-hub/screener/analyst_strong_buy_stocks/'
url14 = 'https://finance.yahoo.com/research-hub/screener/top_stocks_owned_by_ray_dalio/'
url15 = 'https://finance.yahoo.com/research-hub/screener/latest_analyst_upgraded_stocks/'
url16 = 'https://finance.yahoo.com/research-hub/screener/top_stocks_owned_by_warren_buffet/'

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

def GatherStocks():
    stock_symbols = []
    # stock_symbols = ['RDDT' , 'QUBT' , 'PLTR' , 'TSLA' ]
    urlsHub = [url1 , url2 , url3 , url4 , url5 , url6 , url7 , url8 , url9 , url10 , url11  , url12 , url13 , url14 , url15 , url16]
    for n in urlsHub:
        stock_symbols += GetStock(n)
    
    stock_symbols += ['TSSI', 'WGS', 'RCAT', 'APP', 'KINS', 'AENT', 'WLFC', 'CANG', 'BYRN', 'RKLB', 'SUPV', 'RDW', 'RDDT', 'ETON', 'PLTR', 'RGTI', 'QUBT', 'EXOD', 'EAT', 'NN', 'EUDA', 'DAVE', 'CRDO', 'CLS', 'BMA', 'ALLT', 'REAL', 'GGAL', 'MTEK', 'VST', 'BBAR', 'WAVE', 'LFVN', 'MESO', 'AGX', 'PDEX', 'ICLK', 'LUNR', 'CVNA', 'RAIL', 'TLN', 'MSTR', 'UI', 'SEI', 'SMTC', 'DSP', 'BKTI', 'IPX', 'ADMA', 'HOOD', 'SMWB', 'PPTA', 'QFIN', 'IONQ', 'TATT', 'SE', 'GEV', 'EDN', 'OXBR', 'TPC', 'INSG', 'SOUN', 'DOGZ', 'PL', 'YPF', 'PRM', 'ARQT', 'CMPO', 'ECOR', 'TECX', 'USLM', 'TARS', 'SFM', 'INOD', 'RZLT', 'CLBT', 'ZETA', 'CRVS', 'UAL', 'DDL', 'SMR', 'JVA', 'RSI', 'TPB', 'FTAI', 'VRNA', 'QTWO', 'ELMD', 'PRTH', 'NTRA', 'PRAX', 'KOD', 'COMM', 'AVPT', 'APEI', 'CAVA', 'EOSE', 'SPOT', 'FLXS', 'NVDA']

    stock_symbols = list(set(stock_symbols))
    return stock_symbols
stock_symbols += GatherStocks()
stock_symbols = list(set(stock_symbols))

print(stock_symbols)
# Initialize a list to store data
data = []

# Fetch data for each ticker
def GetTicker(months):
    i = 0
    for ticker in stock_symbols:
        i += 1
        if (i % 10 == 0):
            time.sleep(10)
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Get sector, industry, and recent price change
            sector = info.get("sector", "N/A")
            industry = info.get("industry", "N/A")
            recent_price = stock.history(period=f"{months}mo")  # Get 1-month price history
            
            # Calculate performance (percentage change)
            if not recent_price.empty:
                price_change = (recent_price["Close"][-1] - recent_price["Close"][0]) / recent_price["Close"][0] * 100
            else:
                price_change = None

            # Append the data
            data.append({"Ticker": ticker, "Sector": sector, "Industry": industry, "Price Change (%)": price_change})
        except Exception as e:
            pass

# Create a DataFrame

def RunIndustry(months , SP500 = False):
    
    GetTicker(months)
    df = pd.DataFrame(data)

    # Group by Sector and Industry to analyze trends
    sector_trends = df.groupby("Sector")["Price Change (%)"].mean().sort_values(ascending=False)
    industry_trends = df.groupby("Industry")["Price Change (%)"].mean().sort_values(ascending=False)

    # Display the trending sector and industry
    print("Trending Sectors:")
    print(sector_trends)
    print("\nTrending Industries:")
    print(industry_trends)
    if SP500:
        sector_trends.to_csv(f"sector_trendsSP500.csv", header=False)
        industry_trends.to_csv(f"industry_trendsSP500.csv", header=False)
    else:
        sector_trends.to_csv(f"sector_trends{months}.csv", header=False)
        industry_trends.to_csv(f"industry_trends{months}.csv", header=False)

RunIndustry(1)
data = []
RunIndustry(3)
stock_symbols = stocksSP500
RunIndustry(1  , SP500 = True)
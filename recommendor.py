import requests
import financedata
import dataprovider

import re
import betterstokks

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
stock_symbols += [
    'QUBT', 'MVST', 'RCAT', 'MNPR', 'SOUN', 'ZVIA', 'NOTV', 'ATOM',
    'CRNC', 'STIM', 'VRAR', 'ECOR', 'CHRS', 'SLQT', 'PODC', 'QBTS',
    'REAL', 'ACHR', 'KOD', 'SUPV', 'HUT', 'VUZI', 'FOA', 'IONQ', 'VOR',
    'NRXP', 'PSTX', 'KOPN', 'VVOS', 'NPCE', 'CCRD', 'LUNR', 'PLBY', 'AVXL',
    'PRCH', 'EVEX', 'RKLB', 'VCSA', 'FBRX', 'CRK', 'ATRA', 'JOBY', 'LPTH',
    'VSTM', 'CMRX', 'OM', 'UPLD', 'BBAI', 'UNCY', 'ALAB', 'LVO', 'BFLY',
    'HOOD', 'EDN', 'RVPH', 'OPFI', 'SMWB', 'QNCX', 'CSBR', 'PLTR', 'OLO',
    'GH', 'RDDT', 'ETON', 'EHTH', 'ONDS', 'CDTX', 'AS', 'URBN', 'ALGT',
    'BROS', 'WRBY', 'BCOV', 'PL', 'AADI', 'CLS', 'ZENV', 'EOSE', 'MIND',
    'XLO', 'YPF', 'EAT', 'SABS', 'ESOA', 'AISP', 'NTRP', 'BLIN', 'LINK',
    'ANGO', 'BRZE', 'LNSR', 'TPR', 'RRC', 'SEI', 'RSSS', 'BYRN', 'TZOO',
    'SKIL', 'TBRG', 'TENX', 'EQT', 'ALLK', 'DXPE', 'FULC', 'RBLX', 'LRN',
    'UAL', 'ALK', 'AR', 'FGEN', 'BBAR', 'GCO', 'MBLY', 'MGX', 'CRESY',
    'PHR', 'KRMD', 'NEOV', 'LFVN', 'HTCR', 'NRGV', 'EGAN', 'PAM', 'TARS',
    'KLTR', 'VITL', 'ALNT', 'VCYT', 'CXAI', 'NFE', 'CCB', 'GDYN', 'SRFM',
    'MEOH', 'PYCR', 'MRVL', 'AIP', 'SPIR', 'LQDT', 'IKT', 'SMTC', 'GB',
    'DK', 'GEO', 'GRND', 'SFIX', 'ADPT', 'AAL', 'LC', 'FNA', 'EXFY', 'SOFI',
    'SKYT', 'ADTN', 'BE', 'GRCE', 'CXM', 'IMMX', 'VCEL', 'XMTR', 'FSLY',
    'RNXT', 'FTK', 'APYX', 'BB', 'FIVE', 'PTON', 'NATL', 'ASAN', 'NGS',
    'DMAC', 'ARHS', 'PDEX', 'RGEN', 'AKBA', 'GRAL', 'GKOS', 'PUMP', 'ALTR',
    'GTLS', 'SIBN', 'NTRA', 'GOOGL', 'RBOT', 'LOMA', 'TWLO', 'CBRL', 'ICL',
    'FTI', 'AXGN', 'ELF', 'CDZI', 'APEI', 'FSTR', 'EMBC', 'LOVE', 'WMT',
    'UNFI', 'CNVS', 'AKYA', 'BRLT', 'ACAD', 'GPRK', 'RDW', 'CYRX', 'SSYS',
    'RSI', 'UTI', 'CURV', 'GMED', 'CAE', 'DKL', 'AI', 'DAKT', 'VLRS', 'HNST',
    'OSPN', 'C', 'ENFN', 'SONO', 'CRS', 'GPOR', 'HPE', 'SNCY', 'ALRM', 'SKX',
    'RMNI', 'AZTA', 'BKSY', 'NVTS', 'NBIX', 'ELTX', 'VLN', 'YELP', 'MDXG',
    'CHGG', 'NET', 'RNGR', 'JBL', 'AFRM', 'DLNG', 'CEPU', 'OKTA', 'NXT',
    'CTOR', 'NTGR', 'TNDM', 'ATLC', 'PEGA', 'WK', 'WEAV', 'FVRR', 'SHOP',
    'SYM', 'FNKO', 'RPID', 'CEVA', 'EFXT', 'WGS', 'VSCO', 'VIR', 'GHM',
    'SONY', 'BBCP', 'ESQ', 'ATEN', 'TASK', 'NEXT', 'GCMG', 'DHX', 'AMPL',
    'SNEX', 'AZEK', 'LAKE', 'MXCT', 'BMA', 'PFIE', 'INTA', 'RVSB', 'CZWI',
    'ACVA', 'ANET', 'SNOW', 'FWONK', 'OOMA', 'BARK', 'YMM', 'CXT', 'CFLT',
    'TAC', 'CENT', 'APLS', 'SYF', 'QDEL', 'INN', 'CHWY', 'SQ', 'MLAB',
    'PMTS', 'ATGE', 'ARTL', 'ANTX', 'ETR', 'GL', 'ESTC', 'LZB', 'BSX',
    'DMRC', 'HIMS', 'FOUR', 'DUOT', 'WWW', 'RMBS', 'GRPN', 'IRMD', 'BKR',
    'PRTS', 'TNXP', 'FOXA', 'LITE', 'MUFG', 'UFCS', 'LFCR', 'AROC', 'OMI',
    'WSM', 'FPI', 'PRDO', 'USAC', 'SUPN', 'PRIM', 'REVG', 'BFRI', 'SLNG',
    'DTST', 'ALGM', 'KD', 'BBW', 'JILL', 'GIFI', 'WFC', 'EE', 'PRKS', 'PSTG',
    'CCL', 'SHCO', 'EXE', 'USEG', 'KGS', 'OPBK', 'RGP', 'CAKE', 'NEO',
    'BRKR', 'FSS', 'FTNT', 'DEC', 'XERS', 'GBX', 'CAPL', 'MGNI', 'APG',
    'PARR', 'FHN', 'CQP', 'SLAB', 'FUN', 'RLX', 'HLVX', 'DBX', 'TKNO', 'VFC',
    'KN', 'PLNT', 'K', 'FTAI', 'RIVN', 'TECX', 'TGS', 'WBD', 'CVRX', 'NARI',
    'FSK', 'FWONA', 'TH', 'DCTH', 'RICK', 'ATEC', 'RLJ', 'GOCO', 'RXRX',
    'MRBK', 'FSFG', 'BLFS', 'ALTO', 'HQY', 'CTRN', 'MXL', 'WHR', 'A', 'SMFG',
    'DFS', 'VERX', 'HCP', 'KVYO', 'CALM', 'NRG', 'PROV', 'PAY', 'KRON',
    'TGLS', 'SYNA', 'BBSI', 'AAP', 'WLKP', 'WW', 'BBIO', 'INGN', 'MPLX',
    'FINV', 'ULCC', 'OBDE', 'STT', 'IRBT', 'KMX', 'BILL', 'TECH', 'SLM',
    'TPB', 'TDOC', 'HRMY', 'SVCO', 'LUV', 'BCSF', 'SFM', 'PLUG', 'EB', 'PTC',
    'XPO', 'GO', 'BAM', 'CNC', 'OMF', 'CLPT', 'TTI', 'OSIS', 'BKV', 'PVH',
    'BLX', 'TTMI', 'LZ', 'TS', 'BBVA', 'PGNY', 'KTOS', 'LPX', 'DVAX'
]

stock_symbols = list(set(stock_symbols))
file_path = "Recommendor.txt"
betterstokks.WriteToFileAverage(stock_symbols , file_path , timers=True )
import read
read.StoreData("Recommendor.csv" , file_path)

#  One month 
file_path = "Recommendor1month.txt"
betterstokks.WriteToFileAverage(stock_symbols , file_path , timers=True  , months=1)
read.StoreData("Recommendor1month.csv" , file_path)
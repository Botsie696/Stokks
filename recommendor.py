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

file_path = "Recommendor.txt"
betterstokks.WriteToFileAverage(stock_symbols , file_path , timers=True )
import read
read.StoreData("Recommendor.csv" , file_path)
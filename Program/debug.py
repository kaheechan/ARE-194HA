import function as fx
import pandas as pd

FilePath = "RawData/AMZN/AMZN.csv"
# First Tool Box:
PreparationObject = fx.Preparation(FilePath)

# Tools: To Build The First Layer
Price = PreparationObject.stock_price()
Date = PreparationObject.stock_date()
Low = PreparationObject.stock_low()
High = PreparationObject.stock_high()

# Second Tool Box:
IngestionObject = fx.Ingestion(Price, Low, High)

# Tools: To Build The Second Layer
SMA10 = IngestionObject.sma_10()
SMA20 = IngestionObject.sma_20()
SMA50 = IngestionObject.sma_50()
SMA100 = IngestionObject.sma_100()
SMA200 = IngestionObject.sma_200()

RSI = IngestionObject.relative_strength_index()
UBB = IngestionObject.upper_bollinger_twenty()
LBB = IngestionObject.lower_bollinger_twenty()

EMA13 = IngestionObject.ema_thirteen()
EMA25 = IngestionObject.ema_twentyfive()

ATR = IngestionObject.average_true_range()
CE = IngestionObject.chandelier_exit()

TSI = IngestionObject.true_strength_index()

# Note: Combine Columns All Together and Rename All the Columns
MainColumns = [Date, Price, SMA10, SMA20, SMA50, SMA100, SMA200, EMA13, EMA25, RSI, UBB, LBB, ATR, CE, TSI]
ColumnNames = ['Date', 'Price', 'SMA10', 'SMA20', 'SMA50', 'SMA100', 'SMA200', 'EMA13', 'EMA25', 'RSI', 'UBB', 'LBB', 'ATR', 'CE', 'TSI']
MainDF = pd.concat(MainColumns, axis=1)
MainDF.columns = ColumnNames if len(MainDF.columns) == len(ColumnNames) else None




import pandas as pd
import yfinance as yf
import sqlite3 as sq
from dataclasses import dataclass
from datetime import datetime

class Ingestion: # Focus on SPX
    def __init__(self):
        self.close_data = self.close_data()

    def stock_data(self): # Print all the Data of the Stock Ticker
        StockData = yf.download('^GSPC', start='2020-01-01', end=datetime.now().strftime('%Y-%m-%d'))
        return StockData

    # Task: Get Open, High and Low Data

    def close_data(self): # Get all the Stock Data for Close
        CloseData = self.stock_data()['Close']
        return CloseData

    # Strategy One: Moving Averages
    # Example of Moving Averages
    def sma_10(self): # Ten Day Moving Average
        SMA10 = self.close_data.rolling(window=10).mean()
        return SMA10

    def sma_20(self):
        SMA20 = self.close_data.rolling(window=20).mean()
        return SMA20

    # Task: Do SMAFifty, SMAOneHundred, SMATwoHundred
    def sma_50(self):
        SMA50 = self.close_data.rolling(window=20).mean()
        return SMA50

    def sma_100(self):
        SMA100 = self.close_data.rolling(window=100).mean()
        return SMA100

    def sma_200(self):
        SMA200 = self. close_data.rolling(window=100).mean()
        return SMA200

    # Strategy Two: Mean Reversion
    def std_twenty(self):
        STDTwenty = self.close_data.rolling(window=20).std()
        return STDTwenty

    def upper_bollinger_twenty(self):
        UpperBollingerTwenty = self.sma_20() + self.std_twenty() * 2
        return UpperBollingerTwenty

    # Task: We need Two Bands, One Upper Band and One Lower Band. I coded the Upper Band, and you can do the Lower Band
    def lower_bollinger_twenty(self):
        # Your Code
        # Note: You should subtract the sma_twenty by the std_twenty() * 2
        pass

    def ema_twelve(self):
        TwelveDays = self.close_data.ewm(span=12, adjust=False).mean()
        return TwelveDays



# Inserting Data by Using SQL Database
@dataclass
class Insertion:
    ColumnName: str
    ColumnData: pd.Series | pd.DataFrame
    Connection: sq.Connection

    def insert_data(self):
        self.ColumnData.to_sql(self.ColumnName, self.Connection, if_exists='replace', index=True)
        self.Connection.commit()

    def compare_data(self):
        Query = "SELECT * FROM MainDF WHERE \"SMA10\" > \"SMA20\""
        FilteredData = pd.read_sql_query(Query, self.Connection)
        return FilteredData





















































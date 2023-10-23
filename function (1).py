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
        LowerBollingerTwenty= self.sma_20() + self
        # Your Code
        # Note: You should subtract the sma_twenty by the std_twenty() * 2
        pass

    def ema_twelve(self):
        TwelveDays = self.close_data.ewm(span=12, adjust=False).mean()
        return TwelveDays
    def ema26(self):
        TwentysixDays= self.close_data.ewm(span=12, adjust= False).mean()
        return TwentysixDays

#Strtegy Indicators
#Moving Average Strategy
    def moving_average_indicator(self): #data needed for indicator
        SMA50= self.sma_50()
        SMA200= self.sma_200()
    #execute the strategy
        golden_cross_signal= SMA50>SMA200 #buy signal
        return golden_cross_signal
        death_cross_signal = SMA50 < SMA200 #sell signal
        return death_cross_signal

#RSI Strategy
    def RSI_indicator(self, period=14): #data needed for indicator
        close_data= self.close_data()
        # price differences between each day's closing price
        # and the previous day's closing price
        price_diff = close_data.diff(1)

        # Calculate capital gains and losses
        gains = price_diff.where(price_diff > 0, 0)
        losses = -price_diff.where(price_diff < 0, 0)

        # Calculate average gains and losses over 14 days (typical measure for this strategy)
        avg_gain = gains.rolling(window=14).mean()
        avg_loss = losses.rolling(window=14).mean()

        # Calculate the relative strength (RS)
        rs = avg_gain / avg_loss

        # Calculate the RSI
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def rsi_bollinger_strategy(self):
        # calculate rsi of stock
        rsi = self.rsi()
        # Calculate the lower Bollinger Band based on 20-day
        #SMA and 2 times the 20 day standard deviation
        sma20 = self.sma_20()
        std20 = self.std_twenty()
        lower_bollinger = sma20 - 2 * std20
        return lower_bollinger

    #this considers both RSI and Bollinger Bands.
    def combined_trading_strategy(self):
        rsi = self.rsi() #calculate's stock rsi from 0 to 100 scale
        upper_bollinger = self.upper_bollinger_twenty() #calculates upper bollinger band
        lower_bollinger = self.lower_bollinger_twenty() #calculates lower bollinger band

        trading_actions = [] #stores trading actions/ positions taken
        in_position = False #track if we're holding a position

        #loop through the stock data to implement both strategies
        for date, price, rsi_value in zip(rsi.index, self.close_data, rsi):
            #Buy if stock price is below lower bollinger band AND RSI is 30 or lower
            if price < lower_bollinger[date] and rsi_value <= 30:
                if not in_position: #if we're already in a position so we can buy the stock
                    trading_actions.append((date, "Buy")) #add a buy action
                    in_position = True # Set to True to indicate we're taking a position
            elif price> lower_bollinger[date] and rsi_value >= 70: #sell signal
                if in_position:
                    trading_actions.append((date, "Sell")) #sell if meets the criteria
                    in_position = False #updates that we are not in a position
        return trading_actions

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





















































import pandas as pd
import sqlite3 as sq
from dataclasses import dataclass
from datetime import datetime

# First Layer of the House
@dataclass
class Preparation:
    FilePath: str

    def __post_init__(self): # Container Function
        self.stock_data = self.stock_data()

    def stock_data(self):
        StockData = pd.read_csv(self.FilePath)

        # Rename DataFrame
        StockData.columns = ['PERMNO', 'Date', 'Low', 'High', 'Price', 'Return']
        return StockData

    def stock_low(self):
        StockLow = self.stock_data['Low']
        return StockLow

    def stock_high(self):
        StockHigh = self.stock_data['High']
        return StockHigh

    def stock_price(self):  # Get all the Stock Data for Close
        StockPrice = self.stock_data['Price']
        return StockPrice

    def stock_date(self):  # Get stock dates from start to end
        StockDate = self.stock_data['Date']
        return StockDate

    def stock_return(self):
        StockReturn = self.stock_data['Return']
        return StockReturn

@dataclass
class Ingestion: # Focus on SPX
    CloseData: pd.DataFrame | pd.Series
    LowData: pd.DataFrame | pd.Series
    HighData: pd.DataFrame | pd.Series

    def __post_init__(self):
        self.close_data = self.CloseData
        self.low_data = self.LowData
        self.high_data = self.HighData

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
        SMA50 = self.close_data.rolling(window=50).mean()
        return SMA50

    def sma_100(self):
        SMA100 = self.close_data.rolling(window=100).mean()
        return SMA100

    def sma_200(self):
        SMA200 = self. close_data.rolling(window=200).mean()
        return SMA200

    # Strategy Two: Mean Reversion
    def std_twenty(self):
        STDTwenty = self.close_data.rolling(window=20).std()
        return STDTwenty

    def ema_twelve(self):
        TwelveDays = self.close_data.ewm(span=12, adjust=False).mean()
        return TwelveDays

    def ema_twentysix(self):
        TwentySixDays = self.close_data.ewm(span=12, adjust=False).mean()
        return TwentySixDays

    def relative_strength_index(self):
        CloseData = self.close_data
        PriceDiff = CloseData.diff()

        Gains = PriceDiff.where(PriceDiff > 0, 0)
        Losses = -PriceDiff.where(PriceDiff < 0, 0)

        AvgGain = Gains.rolling(window=14).mean()
        AvgLoss = Losses.rolling(window=14).mean()

        RelativeStrength = AvgGain / AvgLoss
        RelativeStrengthIndex = 100 - (100 / (1 + RelativeStrength))

        return RelativeStrengthIndex

    def upper_bollinger_twenty(self):
        UpperBollingerTwenty = self.sma_20() + self.std_twenty() * 2
        return UpperBollingerTwenty

    # Task: We need Two Bands, One Upper Band and One Lower Band. I coded the Upper Band, and you can do the Lower Band
    def lower_bollinger_twenty(self):
        LowerBollingerTwenty = self.sma_20() - self.std_twenty()
        return LowerBollingerTwenty

    def average_true_range(self):
        HighLowDiff = self.high_data - self.low_data
        HighCloseDiff = (self.high_data - self.close_data.shift()).abs()
        LowCloseDiff = (self.low_data - self.close_data.shift()).abs()

        Range = pd.concat([HighLowDiff, HighCloseDiff, LowCloseDiff], axis=1)
        TrueRange = Range.max(axis=1)
        AverageTrueRange = TrueRange.rolling(window=14).mean()
        return AverageTrueRange

    def chandelier_exit(self):
        HighestHigh = self.high_data.rolling(window=14).max()
        AverageTrueRange = self.average_true_range()
        ChandelierExit = HighestHigh - AverageTrueRange * 3
        return ChandelierExit

    def true_strength_index(self):
        pass

@dataclass
# Boolean Class
class Calculation:
    MainDF: pd.DataFrame | pd.Series

    def golen_cross_signal(self):
        SMA50 = self.MainDF['SMA50']
        SMA200 = self.MainDF['SMA200']

        GoldenCrossSignal = SMA50 > SMA200
        return GoldenCrossSignal

    def death_cross_signal(self):
        SMA50 = self.MainDF['SMA50']
        SMA200 = self.MainDF['SMA200']

        DeathCrossSignal = SMA50 < SMA200
        return DeathCrossSignal

    def overbought_signal(self):
        IsOverbought = self.MainDF['RSI'] > 70
        return IsOverbought

    def oversold_signal(self):
        IsOversold = self.MainDF['RSI'] < 30
        return IsOversold

    def low_bollinger_signal(self):
        Price = self.MainDF['Price']
        LowerBollinger = self.MainDF['LBB']

        # HasLowerSignal = True -> Price < LowerBollinger
        HasLowerSignal = Price < LowerBollinger
        return HasLowerSignal

    def high_bollinger_signal(self):
        Price = self.MainDF['Price']
        HigherBollinger = self.MainDF['UBB']

        # HasHigherSignal = True -> Price > HigherBollinger
        HasHigherSignal = Price > HigherBollinger
        return HasHigherSignal

    def chandelier_exit_long(self):
        Price = self.MainDF['Price']
        ChandelierExit = self.MainDF['CE']
        ChandelierExitLong = Price < ChandelierExit
        return ChandelierExitLong

class Combination:
    pass
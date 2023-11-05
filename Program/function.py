import numpy as np
import pandas as pd
import sqlite3 as sq
from dataclasses import dataclass
from datetime import datetime

import icecream as ic
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
        SMA200 = self.close_data.rolling(window=200).mean()
        return SMA200

    # Strategy Two: Mean Reversion
    def std_twenty(self):
        STDTwenty = self.close_data.rolling(window=20).std()
        return STDTwenty

    def ema_thirteen(self, Data=None):
        if Data is None:
            ThirteenDays = self.close_data.ewm(span=13, adjust=False).mean()
        else:
            ThirteenDays = Data.ewm(span=13, adjust=False).mean()
        return ThirteenDays

    def ema_twentyfive(self, Data=None):
        if Data is None:
            TwentyFiveDays = self.close_data.ewm(span=25, adjust=False).mean()
        else:
            TwentyFiveDays = Data.ewm(span=25, adjust=False).mean()
        return TwentyFiveDays

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
        LowerBollingerTwenty = self.sma_20() - self.std_twenty() * 2
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
        PriceDiff = self.close_data.diff()
        EMA1 = self.ema_twentyfive(PriceDiff)
        EMA2 = self.ema_thirteen(EMA1)
        PriceDiffAbs = PriceDiff.abs()
        EMA1A = self.ema_twentyfive(PriceDiffAbs)
        EMA2A = self.ema_thirteen(EMA1A)
        TSI = EMA2 / EMA2A * 100
        return TSI

@dataclass
# Boolean Class
class Calculation:
    MainDF: pd.DataFrame | pd.Series

    def golden_cross_signal(self):
        SMA50 = self.MainDF['SMA50']
        SMA200 = self.MainDF['SMA200']

        GoldenCrossSignal = SMA50 > SMA200
        return GoldenCrossSignal

    def death_cross_signal(self):
        SMA50 = self.MainDF['SMA50']
        SMA200 = self.MainDF['SMA200']

        DeathCrossSignal = SMA50 < SMA200
        return DeathCrossSignal

    def rsi_overbought(self):
        IsOverbought = self.MainDF['RSI'] > 70
        return IsOverbought

    def rsi_oversold(self):
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

    def tsi_overbought(self):
        IsOverbought = self.MainDF['TSI'] > 25
        return IsOverbought

    def tsi_oversold(self):
        IsOversold = self.MainDF['TSI'] < -25
        return IsOversold

@dataclass
class Combination:
    MainDF: pd.DataFrame | pd.Series
    TestDF: pd.DataFrame | pd.Series
    BooleanDF: pd.DataFrame | pd.Series

    def __post_init__(self):
        self.boolean_output = self.BooleanDF[['Hold', 'Buy', 'Sell']]
        self.boolean_cases = self.BooleanDF.drop(['Hold', 'Buy', 'Sell'], axis=1) # All 256 cases

    def convert_tuple(self):
        Data = np.array(self.boolean_cases, dtype=bool)
        return tuple(map(tuple, Data))

    def convert_list(self):
        Data = np.array(self.boolean_output)
        return tuple(map(tuple, Data))

    def convert_dict(self):
        Dict = {}
        BooleanOutput = self.convert_list()
        BooleanCases = self.convert_tuple()
        for Output, Case in zip(BooleanOutput, BooleanCases):
            Dict[Case] = Output
        return Dict

    def convert_output(self):
        TestOutputs = []
        Mapping = self.convert_dict()
        Cases = self.TestDF
        for Index, Value in Cases.iterrows():
            Test = tuple(Value)
            TestOutput = Mapping.get(Test, "Invalid Output")
            TestOutputs.append(TestOutput)
        return TestOutputs

    # def __post_init__(self):
    #     TestColumnNames = self.TestDF.columns
    #     FirstColumn = self.TestDF[TestColumnNames[0]].apply(lambda x: '1' if x else '0')
    #     for ColumnName in TestColumnNames[1:]:
    #         FirstColumn += self.TestDF[ColumnName].apply(lambda x: '1' if x else '0')
    #     self.combined_column = FirstColumn.astype(int)
    #
    # def decode_boolean(self):
    #     CombinedColumn = self.combined_column.apply(lambda x: int(str(x), 2))
    #     return CombinedColumn
    #
    # # Use .iloc -> BooleanDF Result
    # def decode_execution(self):
    #     CombinedColumn = self.decode_boolean()
    #     DecisionMatrix = self.BooleanDF[['Hold', 'Buy', 'Sell']]
    #     Executions = []
    #     for TestValue in CombinedColumn:
    #         print(TestValue)
    #
    #     return Executions
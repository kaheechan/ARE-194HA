import function as fx
import pandas as pd

from icecream import ic

# Goal: Building a House Layer By Layer
if __name__ == "__main__":
    FilePath = "RawData/AMZN/AMZN.csv"
    BooleanPath = "File/BooleanTable.csv"

    # Make BooleanTable -> DataFrame
    BooleanDF = pd.read_csv(BooleanPath)

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
    MainDF = pd.DataFrame(
        {
            "Date": Date,
            "Price": Price,
            "SMA10": SMA10,
            "SMA20": SMA20,
            "SMA50": SMA50,
            "SMA100": SMA100,
            "SMA200": SMA200,
            "EMA13": EMA13,
            "EMA25": EMA25,
            "RSI": RSI,
            "UBB": UBB,
            "LBB": LBB,
            "ATR": ATR,
            "CE": CE,
            "TSI": TSI
        }
    )
    MainDF.columns = ColumnNames if len(MainDF.columns) == len(ColumnNames) else None

    # Note: Make DataFrame to CSV, Processing Data Set, So We Can Visualize Our Data
    MainDF.to_csv("File/Level2.csv")

    # Third Tool Box:
    CalculationObject = fx.Calculation(MainDF)

    # Tools: To Build The Third Layer
    GoldenCross = CalculationObject.golden_cross_signal()
    RSIOverbought = CalculationObject.rsi_overbought()
    RSIOversold = CalculationObject.rsi_oversold()
    LowBollinger = CalculationObject.low_bollinger_signal()
    HighBollinger = CalculationObject.high_bollinger_signal()
    ChandelierExit = CalculationObject.chandelier_exit_long()
    TSIOverbought = CalculationObject.tsi_overbought()
    TSIOversold = CalculationObject.tsi_oversold()

    MainColumns = [Date,
                   Price,
                   Low,
                   High]

    MainColumnNames = ['Date',
                       'Price',
                       'Low',
                       'High']

    MainDF = pd.DataFrame(
        {
            "Date": Date,
            "Price": Price,
            "Low": Low,
            "High": High
        }
    )

    MainDF.columns = MainColumnNames if len(MainDF.columns) == len(MainColumnNames) else None
    MainDF.to_csv("File/Level3.csv") # Date Price

    TestColumns = [
        RSIOverbought,
        RSIOversold,
        TSIOverbought,
        TSIOversold,
        LowBollinger,
        HighBollinger,
        GoldenCross,
        ChandelierExit
        ]

    TestColumnNames = [
        'RSIOverbought',
        'RSIOversold',
        'TSIOverbought',
        'TSIOversold',
        'LowBollinger',
        'HighBollinger',
        'GoldenCross',
        'ChandelierExit'
    ]

    # Save to MainDF
    TestDF = pd.DataFrame(
        {
            "RSIOverbought": RSIOverbought,
            "RSIOversold": RSIOversold,
            "TSIOverbought": TSIOverbought,
            "TSIOversold": TSIOversold,
            "LowBollinger": LowBollinger,
            "HighBollinger": HighBollinger,
            "GoldenCross": GoldenCross,
            "ChandelierExit": ChandelierExit
        }
    )

    # Save to TestDF
    TestDF.columns = TestColumnNames if len(TestDF.columns) == len(TestColumnNames) else None
    TestDF.to_csv("File/Level4.csv") #

    # ic(TestDF)

    # Forth Tool Box:
    CombinationObject = fx.Combination(MainDF, TestDF, BooleanDF)
    OutputData = CombinationObject.convert_output()
    OutputDF = pd.DataFrame(OutputData)
    OutputDF = pd.concat([TestDF, OutputDF], axis=1)
    OutputDF.to_csv("File/Output.csv")

    # Debug
    DebugDF = pd.DataFrame(
        {
            "LBB": LBB,
            "UBB": UBB,
            "LowBollinger": LowBollinger,
            "HighBollinger": HighBollinger
        }
    )

    print(BooleanDF)
    DebugDF.to_csv("File/Debug.csv")

import function as fx
import pandas as pd

from icecream import ic

# Goal: Building a House Layer By Layer
if __name__ == "__main__":
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

    EMA12 = IngestionObject.ema_twelve()
    EMA26 = IngestionObject.ema_twentysix()

    ATR = IngestionObject.average_true_range()
    CE = IngestionObject.chandelier_exit()

    # Note: Combine Columns All Together and Rename All the Columns
    MainColumns = [Date, Price, SMA10, SMA20, SMA50, SMA100, SMA200, EMA12, EMA26, RSI, UBB, LBB, ATR, CE]
    ColumnNames = ['Date', 'Price', 'SMA10', 'SMA20', 'SMA50', 'SMA100', 'SMA200', 'EMA12', 'EMA26', 'RSI', 'UBB', 'LBB', 'ATR', 'CE']
    MainDF = pd.concat(MainColumns, axis=1)
    MainDF.columns = ColumnNames if len(MainDF.columns) == len(ColumnNames) else None

    # Note: Make DataFrame to CSV, Processing Data Set, So We Can Visualize Our Data
    MainDF.to_csv("File/Level2.csv")

    # Third Tool Box:
    CalculationObject = fx.Calculation(MainDF)

    # Tools: To Build The Third Layer
    GoldenCross = CalculationObject.golen_cross_signal()
    # DeathCross = CalculationObject.death_cross_signal()

    MainColumns = [Date, Price, Low, High, GoldenCross]
    ColumnNames = ['Date', 'Price', 'Low', 'High', 'GoldenCross']
    MainDF = pd.concat(MainColumns, axis=1)
    MainDF.columns = ColumnNames if len(MainDF.columns) == len(ColumnNames) else None

    MainDF.to_csv("File/Level3.csv")
    ic(MainDF)





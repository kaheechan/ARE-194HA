import function as fx
import pandas as pd
import sqlite3 as sq

from icecream import ic

if __name__ == "__main__":
    IngestionObject = fx.Ingestion()

    # Note: We can get data from function.py, that we just created, for example...
    ClosePrice = IngestionObject.close_data
    SMA10 = IngestionObject.sma_10() #get sma tool from your inventory
    SMA20 = IngestionObject.sma_20()

    # Task: Code other SMA Below...
    SMA50 = IngestionObject.sma_50()
    SMA100 = IngestionObject.sma_100()
    SMA200 = IngestionObject.sma_200()

    # Note: Combine Columns All Together and Rename All the Columns
    MovingAverages = [ClosePrice, SMA10, SMA20, SMA50, SMA100, SMA200]
    ColumnNames = ['ClosePrice', 'SMA10', 'SMA20', 'SMA50', 'SMA100', 'SMA200']
    MainDF = pd.concat(MovingAverages, axis=1)
    MainDF.columns = ColumnNames if len(MainDF.columns) == len(ColumnNames) else None

    # Note: Store Data into SQL
    Connection = sq.connect('MainDF.db')
    InsertionObject = fx.Insertion('MainDF', MainDF, Connection)
    InsertionObject.insert_data()

    # Note: Retrieve Data from SQL
    ic(InsertionObject.compare_data())

    Connection.commit()
    Connection.close()









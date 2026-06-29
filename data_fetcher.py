import yfinance as yf
import pandas as pd

#function to get historical data for a given ticker and date range, returns a pandas dataframe with the data
def get_historical_data(ticker: str, date_start: str, date_end: str) -> pd.DataFrame:
    
    ticker = ticker.upper() # Ensure ticker is in uppercase format    
    try: #error handling to ensure that the function does not break if there is an issue with data retrieval
        df = yf.download(ticker, start=date_start, end=date_end) #donwload data from yfinance using the ticker and date range provided by the user

        if df.empty: #check if the dataframe is empty, if it is, print a message and return an empty dataframe
            print(f"[DataFetcher] No data found for {ticker}")
            return pd.DataFrame()

        df.index = pd.to_datetime(df.index) # Ensure the index is in datetime format for easier handling of date-based operations

        print(f"[DataFetcher] received {len(df)} days of price data")

        return df

    except Exception as e: #catch any exceptions that may occur during data retrieval and print an error message, then return an empty dataframe
        print(f"[DataFetcher] Error fetching data for {ticker}: {e}")
        return pd.DataFrame()
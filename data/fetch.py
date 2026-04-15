import yfinance as yf
import pandas as pd
import os
import time
import logging


#logging configuration
logging.basicConfig(
    level=logging.INFO,
    format= "%(asctime)s - %(levelname)s - %(message)s"
)



def fetch_stock_data(ticker, start_date, end_date, retries = 3, delay =2):
    """
    Download historical OHLCV data for a given stock ticker.
    Returns a cleaned pandas DataFrame.
    """


    for attempt in range(retries):
        try:
            logging.info(f"Fetching data for {ticker}(Attempt {attempt+1})")
            df = yf.download(ticker, start = start_date, end = end_date, auto_adjust = True, progress=False)
            if df.empty:
             logging.warning(f"No data found for {ticker}")
             return None
            df.dropna(inplace = True)
            logging.info(
                f"{ticker}: {len(df)} rows from {df.index[0].date()} to {df.index[-1].date()}"
            )
            return df
        except Exception as e:
            logging.error(f"Error fetching {ticker}: {e}")
            time.sleep(delay)
    logging.error(f"Failed to fetch data for {ticker} after {retries} attempts")
    return None

    
    
def save_data(df, ticker):
    os.makedirs("data/raw", exist_ok=True)
    path = f"data/raw/{ticker}.csv"
    df.to_csv(path)
    logging.info(f"Saved {ticker} data to {path}")


if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "TSLA"]
    start = "2020-01-01"
    end = "2024-01-01"

    for ticker in tickers:
        df = fetch_stock_data(ticker, start, end)
        if df is not None:
            save_data(df, ticker)
            print(df.head())
            print("---")
    # Rate limiting (avoid API throttling)
    time.sleep(1)
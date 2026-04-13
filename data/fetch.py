import yfinance as yf
import pandas as pd
import os


def fetch_stock_data(ticker, start_date, end_date):
    """
    Download historical OHLCV data for a given stock ticker.
    Returns a cleaned pandas DataFrame.
    """

    print(f"Fetching data for {ticker}...")

    df = yf.download(ticker, start = start_date, end = end_date, auto_adjust = True)

    if df.empty:
        print(f"No data found for {ticker}")
        return None
    df.dropna(inplace = True)

    print(f"Got {len(df)} rows from {df.index[0].date()} to {df.index[-1].date()}")
    return df

def save_data(df, ticker):
    os.makedirs("data/raw", exist_ok=True)
    path = f"data/raw/{ticker}.csv"
    df.to_csv(path)
    print(f"Saved to {path}")


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
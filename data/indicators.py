import pandas as pd
import matplotlib.pyplot as plt



def calculate_sma(dataFrame,columnName,ticker,period):

    """ Calculate Simple Moving Average for a given stock column. 

        Args:
        dataFrame: pandas DataFrame with stock data
        columnName: price column e.g. 'Close'
        ticker: stock ticker e.g. 'AAPL'
        period: number of days for rolling window e.g. 20

        Returns:
        pandas Series with SMA values

    """

    sma = dataFrame[columnName, ticker].rolling(period).mean()
    return sma

def calculate_ema(dataFrame,cloumnName,ticker, period):
    """ Calculate Exponential Moving Average for a given stock column. 

        Args:
        dataFrame: pandas DataFrame with stock data
        columnName: price column e.g. 'Close'
        ticker: stock ticker e.g. 'AAPL'
        period: number of days for rolling window e.g. 20

        Returns:
        pandas Series with EMA values

    """
    ema = dataFrame[columnName,ticker].ewm(span=period).mean()
    return ema

def calculate_rsi(dataFrame, columnName, ticker, period=14):
    # Step 1: calculate daily price changes
    delta = dataFrame[(columnName, ticker)].diff()
    
    # Step 2: separate gains and losses
    gains = delta.clip(lower=0)
    losses = delta.clip(upper=0).abs()
    
    # Step 3: calculate average gain and loss using EMA
    avg_gain = gains.ewm(span=period, adjust=False).mean()
    avg_loss = losses.ewm(span=period, adjust=False).mean()
    
    # Step 4: calculate RS and RSI
    rs = avg_gain/avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


if __name__ == "__main__":
    dataFrame = pd.read_csv("data/raw/AAPL.csv", header = [0,1], index_col=0, parse_dates=True)
    columnName = "Close"
    ticker = "AAPL"
    sma_20 = calculate_sma(dataFrame,columnName,ticker,20)
    sma_50 = calculate_sma(dataFrame, columnName,ticker, 50)
    ema_20 = calculate_ema(dataFrame,columnName,ticker,20)
    ema_50 = calculate_ema(dataFrame, columnName,ticker, 50)
    rsi_14 = calculate_rsi(dataFrame,columnName,ticker,14)



    print(rsi_14.tail())

    fig, (ax1,ax2) = plt.subplots(2,1, figsize = (12,8), sharex = True)

    #visualisation sma
    dataFrame[('Close', 'AAPL')].plot(ax =ax1,label = 'Close Price', alpha=0.5)
    sma_20.plot(ax=ax1, label='20 Day SMA')
    sma_50.plot(ax=ax1, label='50 Day SMA')
    ax1.set_title("AAPL Close Price with Indicators")
    ax1.set_ylabel("Price (USD)")
    ax1.legend()

    rsi_14.plot(ax=ax2, label='RSI 14', color='purple')
    ax2.axhline(70, color='red', linestyle='--', alpha=0.7)
    ax2.axhline(30, color='green', linestyle='--', alpha=0.7)
    ax2.set_title("RSI 14")
    ax2.set_ylabel("RSI")
    ax2.set_xlabel("Date")
    ax2.legend()

    plt.tight_layout()
    plt.show()

    
    

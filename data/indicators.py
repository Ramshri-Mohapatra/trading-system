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


if __name__ == "__main__":
    dataFrame = pd.read_csv("data/raw/AAPL.csv", header = [0,1], index_col=0, parse_dates=True)
    columnName = "Close"
    ticker = "AAPL"
    sma_20 = calculate_sma(dataFrame,columnName,ticker,20)
    sma_50 = calculate_sma(dataFrame, columnName,ticker, 50)
    ema_20 = calculate_ema(dataFrame,columnName,ticker,20)
    ema_50 = calculate_ema(dataFrame, columnName,ticker, 50)


    

    print(ema_20.tail())
    print(ema_50.tail())

    #visualisation sma
    ax = dataFrame[('Close', 'AAPL')].plot(label = 'Close Price', alpha=0.5)
    sma_20.plot(ax=ax, label='20 Day SMA')
    sma_50.plot(ax=ax, label='50 Day SMA')
    ema_20.plot(ax=ax, label='20 Day EMA')
    ema_50.plot(ax=ax, label='50 Day EMA')

    plt.title("AAPL Close Price EMA and SMA")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.savefig("aapl_sma_plot.png", dpi = 300, bbox_inches = "tight")
    plt.show()

    #visualisation ema
    

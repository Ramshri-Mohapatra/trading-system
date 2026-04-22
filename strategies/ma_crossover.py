import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt


def calculate_sma(dataFrame, column_name, ticker, period):
    dataFrame[(f'SMA_{period}', ticker)] = dataFrame[(column_name,ticker)].rolling(period).mean()
    return dataFrame

def generate_ma_signals(dataFrame):
    print ("SMA_CROSS_STRATEGY")
    dataFrame.columns = dataFrame.columns.droplevel(1)
    dataFrame['signal'] = np.where(dataFrame['SMA_20'] > dataFrame['SMA_50'], 1, -1)
    signal_diff = dataFrame['signal'].diff()
    conditions = [signal_diff == 2, signal_diff == -2]
    choices = [1, -1]
    dataFrame['position'] = np.select(conditions, choices, default=0)
    return dataFrame





if __name__ == "__main__":
    dataFrame = pd.read_csv("data/raw/AAPL.csv", header = [0,1], index_col=0, parse_dates=True)
    columnName = "Close"
    ticker = "AAPL"
    dataFrame  = calculate_sma(dataFrame,columnName,ticker,20)
    dataFrame = calculate_sma(dataFrame,columnName,ticker,50)
    dataFrame = generate_signals(dataFrame)

    


    #visualise signals
    

    dataFrame['Close'].plot(label = 'Close Price', alpha=0.5)
    dataFrame['SMA_20'].plot(label='20 Day SMA')
    dataFrame['SMA_50'].plot(label='50 Day SMA')
    plt.title("AAPL Close Price with Indicators")
    plt.ylabel("Price (USD)")
   

    buys = dataFrame[dataFrame['position'] == 1]
    sells = dataFrame[dataFrame['position'] == -1]


    plt.scatter(buys.index, buys['Close'], marker='^', color='green', s=100, label='Buy')
    plt.scatter(sells.index, sells['Close'], marker='v', color='red', s=100, label='Sell')

    plt.legend()

   
    # create folder if it doesn't exist
    os.makedirs("./strategies/charts", exist_ok=True)

    plt.tight_layout()

    plt.savefig(
      "./strategies/charts/ma_crossover_chart.png",
      dpi=300,
      bbox_inches="tight"
    )
    plt.show()

    

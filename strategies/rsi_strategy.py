import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.indicators import calculate_rsi
import numpy as np
import matplotlib.pyplot as plt


def generate_rsi_signals(dataFrame):
    dataFrame.columns = dataFrame.columns.droplevel(1)
    print("RSI_14_STRATEGY")


    conditions= [(dataFrame['RSI_14'].shift(1) >=30) & (dataFrame['RSI_14'] <30 ),(dataFrame['RSI_14'].shift(1) <70) & (dataFrame['RSI_14'] >=70) ]
    choices = [1,-1]
    dataFrame['position'] = np.select(conditions,choices, default=0) 

    return dataFrame

if __name__ == "__main__":
    TICKER = "AAPL"
    dataFrame = pd.read_csv (f"data/raw/{TICKER}.csv", header=[0,1], index_col=0, parse_dates=True)
    dataFrame['RSI_14'] = calculate_rsi(dataFrame, 'Close', TICKER, 14)
    dataFrame = generate_rsi_signals(dataFrame)

    buys = dataFrame[dataFrame['position'] ==1]
    sells = dataFrame[dataFrame['position'] ==-1]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    dataFrame['Close'].plot(ax=ax1, label='Close Price', alpha=0.5)
    ax1.scatter(buys.index, buys['Close'], marker='^', color='green', s=100, label='Buy')
    ax1.scatter(sells.index, sells['Close'], marker='v', color='red', s=100, label='Sell')
    ax1.legend()

    dataFrame['RSI_14'].plot(ax=ax2, color='orange', label='RSI 14')
    ax2.axhline(70, color='red', linestyle='--', alpha=0.7)
    ax2.axhline(30, color='green', linestyle='--', alpha=0.7)
    ax2.legend()

   
    # create folder if it doesn't exist
    os.makedirs("./strategies/charts", exist_ok=True)

    plt.tight_layout()

    plt.savefig(
      "./strategies/charts/rsi_signals_chart.png",
      dpi=300,
      bbox_inches="tight"
    )
    plt.show()




import pandas as pd
import os
import sys
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from strategies.ma_crossover import calculate_sma, generate_sma_signals
from strategies.rsi_strategy import generate_rsi_signals
from data.indicators import calculate_rsi
import matplotlib.pyplot as plt


def engine(dataFrame, starting_cash,TICKER):
    cash = starting_cash
    shares = 0
    portfolio_values = []

    dataFrame['position'] = dataFrame['position'].shift(1) #inorder to simulate next day buy/sell
    #print(f"DataFrame length: {len(dataFrame)}")
    #print(f"Position column sample:\n{dataFrame['position'].value_counts()}")
    for date, row in dataFrame.iterrows():
      if row['position'] == 1 and shares == 0:
        #print(f"[{TICKER}] BUY  on {date} at Open={row['Open']:.2f}, cash={cash:.2f}, shares={shares}")
        shares = int(cash / row['Open'])
        cash = cash - (shares * row['Open'])
      elif row['position'] == -1:
        #print(f"[{TICKER}] SELL on {date} at Open={row['Open']:.2f}, shares={shares}, cash={cash:.2f}")
        cash = cash + (shares * row['Open'])
        shares = 0

      portfolio_value = cash + (shares * row['Close'])
      portfolio_values.append(portfolio_value)
    
    
   
    portfolio_series = pd.Series(portfolio_values, index = dataFrame.index)
    daily_returns = portfolio_series.pct_change().dropna()

    #Sharpe ratio
    sharpe = (daily_returns.mean()/daily_returns.std())*np.sqrt(252)
    print(f"sharpe ratio: {sharpe:.2f}")

    #Max  drawdown
    rolling_max = portfolio_series.cummax()
    drawdown = (portfolio_series-rolling_max)/rolling_max
    max_drawdown =drawdown.min()
    print(f"Max drawdown: {max_drawdown:.2%}")
    return portfolio_values

if __name__ == "__main__":
    TICKER = "TSLA"
    df_sma= pd.read_csv(f"data/raw/{TICKER}.csv", header=[0,1], index_col=0, parse_dates=True)
    df_rsi= pd.read_csv(f"data/raw/{TICKER}.csv", header=[0,1], index_col=0, parse_dates=True)
    
    calculate_sma(df_sma, 'Close', TICKER, 20)
    calculate_sma(df_sma, 'Close', TICKER, 50)
    generate_sma_signals(df_sma)
    print(f"Starting cash: £10,000 for {TICKER}")
    portfolio_values = engine(df_sma, 10000,TICKER)
    final_value = portfolio_values[-1]
    print(f"Final portfolio value: £{final_value:.2f}")
    print(f"Total return: {((final_value - 10000) / 10000) * 100:.2f}%")
    print("\n")

    df_rsi[('RSI_14',TICKER)] = calculate_rsi(df_rsi, 'Close', TICKER, 14)
    generate_rsi_signals(df_rsi)
    print(f"Starting cash: £10,000 for {TICKER}")
    portfolio_values = engine(df_rsi, 10000,TICKER)
    final_value = portfolio_values[-1]
    print(f"Final portfolio value: £{final_value:.2f}")
    print(f"Total return: {((final_value - 10000) / 10000) * 100:.2f}%")
    print("\n")
    

    
    buy_hold_return = ((df_sma['Close'].iloc[-1] - df_sma['Close'].iloc[0]) / df_sma['Close'].iloc[0]) * 100
    print(f"Buy and hold return: {buy_hold_return:.2f}%") 

    # buy and hold portfolio values
    bh_shares = int(10000 / df_sma['Open'].iloc[0])
    bh_values = pd.Series(
        bh_shares * df_sma['Close'],
        index=df_sma.index
    )

    # buy and hold Sharpe
    bh_daily_returns = bh_values.pct_change().dropna()
    bh_sharpe = (bh_daily_returns.mean() / bh_daily_returns.std()) * np.sqrt(252)
    print(f"Buy and hold Sharpe ratio: {bh_sharpe:.2f}")

    # buy and hold max drawdown
    bh_rolling_max = bh_values.cummax()
    bh_drawdown = (bh_values - bh_rolling_max) / bh_rolling_max
    bh_max_drawdown = bh_drawdown.min()
    print(f"Buy and hold max drawdown: {bh_max_drawdown:.2%}")






    

    
    
import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
import numpy as np
from data.indicators import calculate_rsi
from strategies.ma_crossover import calculate_sma, generate_sma_signals
from strategies.rsi_strategy import generate_rsi_signals
from backtest.engine import engine

st.title("Algorithmic Trading Backtester") # Big title 
ticker = st.sidebar.selectbox("Select Stock", ["AAPL", "MSFT", "TSLA"]) # dropdown in sidebar
strategy = st.sidebar.selectbox ("Select Strategy", ["MA Crossover", "RSI", "Both"])
starting_cash = st.sidebar.number_input("Starting Cash ($)", min_value= 1000, max_value=100000, value = 10000, step = 1000)

#load the data based on ticker
df = pd.read_csv(f"data/raw/{ticker}.csv", header = [0,1], index_col = 0, parse_dates=True)

#run selected strategy

if strategy == "MA Crossover":
    df_strategy = df.copy()
    calculate_sma(df_strategy,'Close',ticker,20)
    calculate_sma(df_strategy, 'Close',ticker, 50)
    generate_sma_signals(df_strategy)
    portfolio_values = engine(df_strategy, starting_cash, ticker)
    

elif strategy == "RSI":
    df_strategy = df.copy()
    df_strategy[('RSI_14', ticker)] = calculate_rsi(df_strategy, 'Close', ticker, 14)
    generate_rsi_signals(df_strategy)
    portfolio_values = engine(df_strategy, starting_cash, ticker)



#show final values
final_value = portfolio_values[-1]
total_return = ((final_value - starting_cash)/ starting_cash) *100

portfolio_series = pd.Series(portfolio_values, index = df_strategy.index)
daily_returns = portfolio_series.pct_change().dropna()
sharpe = (daily_returns.mean()/ daily_returns.std()) * np.sqrt(252)
rolling_max = portfolio_series.cummax()
drawdown = (portfolio_series - rolling_max)/rolling_max
max_drawdown = drawdown.min()

# buy and hold metrics
bh_shares = int(starting_cash/df_strategy['Open'].iloc[0])
bh_values = pd.Series(bh_shares * df_strategy['Close'], index = df_strategy.index)
bh_return = ((bh_values.iloc[-1]- starting_cash) /starting_cash)*100

# display metrics

col1,col2,col3,col4 = st.columns(4)
col1.metric("Final Value", f"£{final_value:.2f}")
col2.metric("Total Return", f"{total_return:.2f}%")
col3.metric("Sharpe Ratio", f"{sharpe:.2f}")
col4.metric("Max Drawdown", f"{max_drawdown:.2%}")

st.metric("Buy & Hold Return", f"{bh_return:.2f}%")

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# price chart with buy/sell signal

buys = df_strategy[df_strategy['position'] == 1]
sells = df_strategy[df_strategy['position'] == -1]

fig = go.Figure()
fig.add_trace(go.Scatter(x =df_strategy.index, y = df_strategy['Close'], name = 'Close Price', line = dict(color = 'blue', width = 1)))
fig.add_trace(go.Scatter(x=buys.index, y=buys['Close'], mode='markers', name='Buy', marker=dict(symbol='triangle-up', size=10, color='green')))
fig.add_trace(go.Scatter(x=sells.index, y=sells['Close'], mode='markers', name='Sell', marker=dict(symbol='triangle-down', size=10, color='red')))
fig.update_layout(title=f"{ticker} Price with {strategy} Signals", xaxis_title="Date", yaxis_title="Price (USD)")
if strategy == "MA Crossover":
    fig.add_trace(go.Scatter(x=df_strategy.index, y=df_strategy['SMA_20'], name='SMA 20', line=dict(color='orange', width=1)))
    fig.add_trace(go.Scatter(x=df_strategy.index, y=df_strategy['SMA_50'], name='SMA 50', line=dict(color='green', width=1)))
st.plotly_chart(fig, use_container_width=True)



# portfolio value vs buy and hold
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df_strategy.index, y=portfolio_series, name='Strategy', line=dict(color='green')))
fig2.add_trace(go.Scatter(x=df_strategy.index, y=bh_values, name='Buy & Hold', line=dict(color='orange')))
fig2.update_layout(title="Portfolio Value vs Buy & Hold", xaxis_title="Date", yaxis_title="Value (£)")
st.plotly_chart(fig2, use_container_width=True)



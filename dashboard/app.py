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
    strategy_data = {"MA Crossover":(df_strategy, portfolio_values)}
    

elif strategy == "RSI":
    df_strategy = df.copy()
    df_strategy[('RSI_14', ticker)] = calculate_rsi(df_strategy, 'Close', ticker, 14)
    generate_rsi_signals(df_strategy)
    portfolio_values = engine(df_strategy, starting_cash, ticker)
    strategy_data = {"RSI":(df_strategy, portfolio_values)}


elif strategy == "Both":
    df_sma = df.copy()
    df_rsi = df.copy()
    calculate_sma(df_sma, 'Close', ticker, 20)
    calculate_sma(df_sma, 'Close', ticker, 50)
    generate_sma_signals(df_sma)

    df_rsi[('RSI_14', ticker)] = calculate_rsi(df_rsi, 'Close', ticker, 14)
    generate_rsi_signals(df_rsi)

    pv_sma = engine(df_sma, starting_cash, ticker)
    pv_rsi = engine(df_rsi, starting_cash, ticker)

    strategy_data = {"MA Crossover": (df_sma, pv_sma), "RSI": (df_rsi, pv_rsi)}

    




#show final values
first_df = list(strategy_data.values())[0][0]
bh_shares = int(starting_cash/ first_df['Open'].iloc[0])
bh_values = pd.Series(bh_shares*first_df['Close'], index = first_df.index)
bh_returns = ((bh_values.iloc[-1]-starting_cash)/starting_cash)*100
bh_ps = pd.Series(list(bh_values), index=first_df.index)
bh_dr = bh_ps.pct_change().dropna()
bh_sharpe = (bh_dr.mean() / bh_dr.std()) * np.sqrt(252)
bh_mdd = ((bh_ps - bh_ps.cummax()) / bh_ps.cummax()).min()
#METRICS
cols = st.columns(len(strategy_data) + 1)
for i, (name, (df_s, pv)) in enumerate(strategy_data.items()):
    ret = ((pv[-1] - starting_cash)/starting_cash)*100
    ps = pd.Series(pv, index=df_s.index)
    dr = ps.pct_change().dropna()
    sh = (dr.mean() / dr.std()) * np.sqrt(252)
    mdd = ((ps - ps.cummax()) / ps.cummax()).min()
    cols[i].subheader(name)
    cols[i].metric("Final Value", f"£{pv[-1]:.2f}")
    cols[i].metric("Total Return", f"{ret:.2f}%")
    cols[i].metric("Sharpe", f"{sh:.2f}")
    cols[i].metric("Max Drawdown", f"{mdd:.2%}")

cols[-1].subheader("Buy & Hold")
cols[-1].metric("Final Value", f"£{bh_values.iloc[-1]:.2f}")
cols[-1].metric("Total Return", f"{bh_returns:.2f}%")
cols[-1].metric("Sharpe", f"{bh_sharpe:.2f}")
cols[-1].metric("Max Drawdown", f"{bh_mdd:.2%}")

                      

import plotly.graph_objects as go
from plotly.subplots import make_subplots
fig = go.Figure()
for name, (df_s, pv) in strategy_data.items():
    fig.add_trace(go.Scatter(x=df_s.index, y=df_s['Close'], name='Close Price', line=dict(color='blue', width=1)))
    buys = df_s[df_s['position'] == 1]
    sells = df_s[df_s['position'] == -1]
    fig.add_trace(go.Scatter(x=buys.index, y=buys['Close'], mode='markers', name=f'{name} Buy', marker=dict(symbol='triangle-up', size=10, color='green')))
    fig.add_trace(go.Scatter(x=sells.index, y=sells['Close'], mode='markers', name=f'{name} Sell', marker=dict(symbol='triangle-down', size=10, color='red')))

fig.update_layout(title=f"{ticker} Price with Signals", xaxis_title="Date", yaxis_title="Price (USD)")
st.plotly_chart(fig, use_container_width=True)

# portfolio value chart
fig2 = go.Figure()
colors = ['green', 'purple']
for i, (name, (df_s, pv)) in enumerate(strategy_data.items()):
    ps = pd.Series(pv, index=df_s.index)
    fig2.add_trace(go.Scatter(x=df_s.index, y=ps, name=name, line=dict(color=colors[i])))

fig2.add_trace(go.Scatter(x=first_df.index, y=bh_values, name='Buy & Hold', line=dict(color='orange')))
fig2.update_layout(title="Portfolio Value vs Buy & Hold", xaxis_title="Date", yaxis_title="Value (£)")
st.plotly_chart(fig2, use_container_width=True)


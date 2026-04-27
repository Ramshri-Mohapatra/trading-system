# Algorithmic Trading Backtester

A Python-based backtesting framework that tests rule-based trading strategies on historical stock data, measures risk-adjusted performance, and visualises results through an interactive dashboard.

**Live demo:** https://trading-system-fegxbv3zb27sfbncazbvuu.streamlit.app/

---

## What it does

- Fetches real historical price data for AAPL, MSFT, and TSLA using Yahoo Finance
- Calculates technical indicators — SMA, EMA, and RSI — from scratch
- Implements two trading strategies with buy/sell signal generation
- Simulates portfolio performance with realistic trade execution (next-day open price)
- Measures performance using Sharpe ratio, max drawdown, and total return
- Compares strategy performance against a buy and hold benchmark
- Displays everything in an interactive Streamlit dashboard

---

## Strategies

**MA Crossover**
Generates a buy signal when the 20-day SMA crosses above the 50-day SMA (golden cross) and a sell signal when it crosses below (death cross).

**RSI Strategy**
Generates a buy signal when RSI crosses below 30 (oversold condition ends) and a sell signal when RSI crosses above 70 (overbought condition begins).

---

## Results

### AAPL (2020–2024)
| Metric | MA Crossover | RSI | Buy & Hold |
|---|---|---|---|
| Total return | 78.88% | 27.27% | 166.77% |
| Sharpe ratio | 0.80 | 0.37 | 0.89 |
| Max drawdown | -27.82% | -25.79% | -31.43% |

### MSFT (2020–2024)
| Metric | MA Crossover | RSI | Buy & Hold |
|---|---|---|---|
| Total return | 38.15% | 87.84% | 143.98% |
| Sharpe ratio | 0.50 | 0.73 | 0.85 |
| Max drawdown | -39.33% | -28.48% | -37.15% |

### TSLA (2020–2024)
| Metric | MA Crossover | RSI | Buy & Hold |
|---|---|---|---|
| Total return | 119.58% | 76.90% | 777.13% |
| Sharpe ratio | 0.66 | 0.54 | 1.14 |
| Max drawdown | -50.03% | -62.66% | -73.63% |

Key finding: RSI outperformed MA Crossover on MSFT on both 
Sharpe ratio and max drawdown, suggesting RSI suits 
range-bound stocks while MA Crossover suits trending assets.
TSLA buy and hold had the best Sharpe (1.14) but required 
surviving a -73% drawdown — psychologically very difficult.

---

## Project structure

```
trading-system/
├── data/
│   ├── fetch.py          # fetches and saves historical OHLCV data
│   ├── indicators.py     # SMA, EMA, RSI calculations
│   └── raw/              # CSV files (gitignored)
├── strategies/
│   ├── ma_crossover.py   # golden cross / death cross strategy
│   └── rsi_strategy.py   # RSI overbought / oversold strategy
├── backtest/
│   └── engine.py         # backtesting engine with performance metrics
├── dashboard/
│   └── app.py            # Streamlit interactive dashboard
├── notebooks/
│   └── exploration.ipynb # data exploration and visualisation
└── requirements.txt
```

---

## How to run locally

**1. Clone the repo**
```bash
git clone https://github.com/Ramshri-Mohapatra/trading-system.git
cd trading-system
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Fetch stock data**
```bash
python data/fetch.py
```

**5. Run the dashboard**
```bash
streamlit run dashboard/app.py
```

---

## Tech stack

- Python 3.11
- pandas, numpy — data manipulation and indicator calculations
- yfinance — historical market data
- Streamlit — interactive dashboard
- Plotly — interactive charts
- matplotlib — static chart generation

---

## Key concepts implemented

- Look-ahead bias prevention — signals are shifted by one day so trades execute at the next day's open price, not the signal day's close
- Sharpe ratio — measures risk-adjusted return (annualised using √252 scaling)
- Max drawdown — measures the largest peak-to-trough decline in portfolio value
- Modular engine design — the backtesting engine is strategy-agnostic and works with any signal generator

---

## What I learned

This project taught me how real backtesting frameworks are structured — separating data fetching, indicator calculation, signal generation, and performance measurement into independent modules. The most important finding was that raw return alone is a poor measure of strategy quality — a strategy returning 78% with a Sharpe of 0.80 and -27% max drawdown tells a more complete story than one returning 163% with higher volatility.
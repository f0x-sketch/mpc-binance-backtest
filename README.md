# MPC Binance Backtest

A secure multi-party computation backtesting tool for cryptocurrency trading strategies using MPyC and Freqtrade.

## Features

- Secure computation of trading signals using MPC
- Integration with Freqtrade's data handling
- Support for Binance historical data
- Custom strategy implementation with secure computations

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from mpc_backtest import MPCBacktester
from example_strategy import SecureMPCStrategy

# Configure backtest
config = {
    'datadir': 'user_data/data',
    'exchange': {
        'name': 'binance',
        'key': '',
        'secret': ''
    }
}

# Initialize
strategy = SecureMPCStrategy()
backtester = MPCBacktester(config, strategy)

# Run backtest
results = await backtester.run_backtest(
    pair='BTC/USDT',
    timeframe='5m',
    timerange='20240101-'
)
```
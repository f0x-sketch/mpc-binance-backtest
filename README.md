# MPC Binance Backtest

A beginner-friendly guide to backtesting cryptocurrency trading strategies with privacy-preserving Multi-Party Computation (MPC).

## What is This Tool?

This tool helps you test your cryptocurrency trading strategies while keeping your strategy details private using advanced encryption. Think of it as a simulator that lets you see how well your trading rules would have worked in the past, but with extra privacy protection.

## Why Use MPC for Backtesting?

- **Privacy**: Your trading strategy stays secret even while testing
- **Security**: Data is encrypted during computations
- **Collaboration**: Work with others without revealing your strategy details

## Getting Started

### Prerequisites

1. Python 3.8 or newer
2. A Binance account (for data access)
3. Basic understanding of trading concepts

### Installation

1. Clone this repository:
```bash
git clone https://github.com/f0x-sketch/mpc-binance-backtest.git
cd mpc-binance-backtest
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

### Basic Usage

1. Set up your configuration:
```python
# config.py
config = {
    'datadir': 'user_data/data',
    'exchange': {
        'name': 'binance',
        'key': 'YOUR_API_KEY',    # Optional for historical data
        'secret': 'YOUR_SECRET'   # Optional for historical data
    }
}
```

2. Create your first strategy:
```python
# my_strategy.py
from example_strategy import SecureMPCStrategy

class MyFirstStrategy(SecureMPCStrategy):
    # Simple moving average crossover
    async def secure_populate_indicators(self, secure_close, secure_volume, mpc):
        # Calculate 20-day and 50-day SMAs
        sma_20 = await self.calculate_sma(secure_close, 20, mpc)
        sma_50 = await self.calculate_sma(secure_close, 50, mpc)
        
        # Generate signals
        entry_signals = []
        exit_signals = []
        
        for i in range(len(secure_close)):
            if i < 50:  # Wait for enough data
                entry_signals.append(mpc.SecInt(0))
                exit_signals.append(mpc.SecInt(0))
                continue
                
            # Buy when 20 SMA crosses above 50 SMA
            entry = sma_20[i] > sma_50[i]
            # Sell when 20 SMA crosses below 50 SMA
            exit = sma_20[i] < sma_50[i]
            
            entry_signals.append(entry)
            exit_signals.append(exit)
            
        return {
            'entry': entry_signals,
            'exit': exit_signals
        }
```

3. Run your backtest:
```python
from mpc_backtest import MPCBacktester
from my_strategy import MyFirstStrategy

async def main():
    strategy = MyFirstStrategy()
    backtester = MPCBacktester(config, strategy)
    
    results = await backtester.run_backtest(
        pair='BTC/USDT',        # Currency pair to test
        timeframe='5m',         # 5-minute candles
        timerange='20240101-'   # From January 1st, 2024
    )
    
    print(results)

# Run the backtest
import asyncio
asyncio.run(main())
```

## Understanding the Results

The backtest results include:
- Total profit/loss
- Number of trades
- Win rate
- Average trade duration
- Maximum drawdown

Example output:
```
Backtest Results:
Total Trades: 42
Profitable Trades: 25 (59.5%)
Total Profit: 3.2%
Average Trade: 0.076%
Max Drawdown: 1.5%
```

## Common Questions

### How do I download historical data?
Use Freqtrade's data download command:
```bash
freqtrade download-data --exchange binance --pairs BTC/USDT ETH/USDT --timeframe 5m
```

### How can I modify the strategy?
Look at example_strategy.py for a template. The main parts to modify are:
- Indicator calculations in secure_populate_indicators()
- Entry and exit conditions
- Risk parameters (stop loss, take profit)

### What's the difference from regular backtesting?
MPC backtesting adds privacy protection by encrypting your strategy's calculations. This is useful when:
- Testing strategies on shared infrastructure
- Collaborating with others
- Protecting intellectual property

## Advanced Topics

- Creating custom indicators with MPC
- Optimizing strategy parameters
- Running distributed backtests
- Implementing risk management

## Need Help?

- Check the [Issues](https://github.com/f0x-sketch/mpc-binance-backtest/issues) section
- Read the [MPyC documentation](https://mpyc.readthedocs.io/)
- Review [Freqtrade docs](https://www.freqtrade.io/)
# MPC Binance Backtest

Privacy-preserving cryptocurrency trading strategy backtester using Multi-Party Computation (MPC).

## Quick Start

```bash
git clone https://github.com/f0x-sketch/mpc-binance-backtest.git
cd mpc-binance-backtest
pip install -r requirements.txt
```

## Setup

1. Create config.json:
```json
{
    "datadir": "user_data/data",
    "exchange": {
        "name": "binance",
        "key": "YOUR_API_KEY",
        "secret": "YOUR_SECRET"
    },
    "pairs": ["BTC/USDT", "ETH/USDT"],
    "timeframe": "5m",
    "strategy_name": "MyStrategy"
}
```

2. Download data:
```bash
freqtrade download-data --exchange binance --pairs BTC/USDT ETH/USDT --timeframe 5m
```

## Create Strategy

Create `strategies/my_strategy.py`:

```python
from mpc_backtest.base_strategy import MPCBaseStrategy

class MyStrategy(MPCBaseStrategy):
    def __init__(self):
        self.sma_short = 20
        self.sma_long = 50
        self.rsi_period = 14

    async def secure_populate_indicators(self, secure_close, secure_volume, mpc):
        # Calculate indicators
        sma_short = await self.calculate_sma(secure_close, self.sma_short, mpc)
        sma_long = await self.calculate_sma(secure_close, self.sma_long, mpc)
        rsi = await self.calculate_rsi(secure_close, self.rsi_period, mpc)
        
        entry_signals = []
        exit_signals = []
        
        for i in range(len(secure_close)):
            entry = (sma_short[i] > sma_long[i]) & (rsi[i] < 30)
            exit = (sma_short[i] < sma_long[i]) | (rsi[i] > 70)
            
            entry_signals.append(entry)
            exit_signals.append(exit)
        
        return {'entry': entry_signals, 'exit': exit_signals}
```

## Run Backtest

Create `run_backtest.py`:

```python
import asyncio
import json
from mpc_backtest import MPCBacktester
from strategies.my_strategy import MyStrategy

async def main():
    with open('config.json') as f:
        config = json.load(f)
    
    strategy = MyStrategy()
    backtester = MPCBacktester(config, strategy)
    
    results = await backtester.run_backtest(
        pair='BTC/USDT',
        timeframe='5m',
        timerange='20240101-'
    )
    
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
```

Run:
```bash
python run_backtest.py
```

## Advanced Strategy Examples

See `examples/` directory for:
- Multiple timeframe strategy
- Machine learning integration
- Custom indicator implementation
- Risk management examples

## Documentation

- [Strategy Development](docs/strategy.md)
- [Indicator Reference](docs/indicators.md)
- [Configuration Guide](docs/config.md)
- [API Reference](docs/api.md)

## License

MIT
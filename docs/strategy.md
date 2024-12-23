# Strategy Development Guide

## Basic Structure
```python
class MyStrategy(MPCBaseStrategy):
    def __init__(self):
        # Define parameters
        pass

    async def secure_populate_indicators(self, secure_close, secure_volume, mpc):
        # Calculate indicators
        # Generate signals
        return {'entry': entry_signals, 'exit': exit_signals}
```

## Available Indicators
- SMA/EMA
- RSI
- MACD
- Bollinger Bands
- Custom indicators

## Best Practices
1. Initialize parameters in __init__
2. Use secure computation for all calculations
3. Handle edge cases
4. Optimize performance

## Example Implementations
See examples/ directory
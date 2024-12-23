from freqtrade.data.history import load_pair_history
from mpyc.runtime import mpc

class MPCBacktester:
    def __init__(self, config, strategy):
        self.config = config
        self.strategy = strategy
        self.mpc = mpc

    async def run_backtest(self, pair, timeframe, timerange):
        data = load_pair_history(
            datadir=self.config['datadir'],
            pair=pair,
            timeframe=timeframe,
            timerange=timerange
        )

        await mpc.start()

        try:
            # Convert to secure types
            secure_close = [mpc.SecFxp(x) for x in data['close']]
            secure_volume = [mpc.SecFxp(x) for x in data['volume']]

            # Get signals
            signals = await self.strategy.secure_populate_indicators(
                secure_close,
                secure_volume,
                mpc
            )

            # Process results
            return await self._process_signals(signals, data)

        finally:
            await mpc.shutdown()

    async def _process_signals(self, signals, data):
        entry_signals = [await mpc.output(s) for s in signals['entry']]
        exit_signals = [await mpc.output(s) for s in signals['exit']]

        trades = []
        position = None

        for i in range(len(data)):
            if entry_signals[i] and not position:
                position = {
                    'entry_price': data['close'][i],
                    'entry_time': data.index[i]
                }
            elif exit_signals[i] and position:
                trades.append({
                    'entry_price': position['entry_price'],
                    'entry_time': position['entry_time'],
                    'exit_price': data['close'][i],
                    'exit_time': data.index[i],
                    'profit_pct': (data['close'][i] - position['entry_price']) / position['entry_price'] * 100
                })
                position = None

        return self._calculate_statistics(trades)
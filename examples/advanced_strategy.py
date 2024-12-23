from mpc_backtest.base_strategy import MPCBaseStrategy

class AdvancedStrategy(MPCBaseStrategy):
    def __init__(self):
        self.sma_short = 20
        self.sma_long = 50
        self.rsi_period = 14
        self.macd_fast = 12
        self.macd_slow = 26
        self.macd_signal = 9
        self.volume_ma = 20

    async def secure_populate_indicators(self, secure_close, secure_volume, mpc):
        # Calculate standard indicators
        sma_short = await self.calculate_sma(secure_close, self.sma_short, mpc)
        sma_long = await self.calculate_sma(secure_close, self.sma_long, mpc)
        rsi = await self.calculate_rsi(secure_close, self.rsi_period, mpc)
        
        # MACD calculation
        macd = await self.calculate_macd(
            secure_close, 
            self.macd_fast, 
            self.macd_slow, 
            self.macd_signal,
            mpc
        )
        
        # Volume analysis
        volume_ma = await self.calculate_sma(secure_volume, self.volume_ma, mpc)
        
        entry_signals = []
        exit_signals = []
        
        for i in range(len(secure_close)):
            if i < self.macd_slow:
                entry_signals.append(mpc.SecInt(0))
                exit_signals.append(mpc.SecInt(0))
                continue

            # Complex entry conditions
            trend_following = sma_short[i] > sma_long[i]
            oversold = rsi[i] < 30
            macd_cross = macd['macd'][i] > macd['signal'][i]
            volume_confirm = secure_volume[i] > volume_ma[i] * 2

            entry = (
                trend_following &
                oversold &
                macd_cross &
                volume_confirm
            )

            # Complex exit conditions
            trend_reversal = sma_short[i] < sma_long[i]
            overbought = rsi[i] > 70
            macd_exit = macd['macd'][i] < macd['signal'][i]

            exit = (
                trend_reversal |
                overbought |
                macd_exit
            )

            entry_signals.append(entry)
            exit_signals.append(exit)

        return {
            'entry': entry_signals,
            'exit': exit_signals
        }

    async def calculate_macd(self, secure_close, fast_period, slow_period, signal_period, mpc):
        fast_ema = await self.calculate_ema(secure_close, fast_period, mpc)
        slow_ema = await self.calculate_ema(secure_close, slow_period, mpc)
        
        macd_line = [f - s for f, s in zip(fast_ema, slow_ema)]
        signal_line = await self.calculate_ema(macd_line, signal_period, mpc)
        
        return {
            'macd': macd_line,
            'signal': signal_line,
            'histogram': [m - s for m, s in zip(macd_line, signal_line)]
        }
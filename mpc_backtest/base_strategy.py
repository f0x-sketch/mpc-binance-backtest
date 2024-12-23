from abc import ABC, abstractmethod

class MPCBaseStrategy(ABC):
    @abstractmethod
    async def secure_populate_indicators(self, secure_close, secure_volume, mpc):
        pass

    async def calculate_sma(self, data, period, mpc):
        result = []
        for i in range(len(data)):
            if i < period:
                result.append(data[i])
                continue
            window_sum = mpc.sum(data[i-period:i])
            result.append(window_sum / period)
        return result

    async def calculate_ema(self, data, period, mpc):
        multiplier = 2 / (period + 1)
        result = [data[0]]
        for i in range(1, len(data)):
            ema = (data[i] * multiplier) + (result[-1] * (1 - multiplier))
            result.append(ema)
        return result

    async def calculate_rsi(self, data, period, mpc):
        changes = [data[i] - data[i-1] for i in range(1, len(data))]
        gains = [max(change, 0) for change in changes]
        losses = [max(-change, 0) for change in changes]

        avg_gain = await self.calculate_sma(gains + [0], period, mpc)
        avg_loss = await self.calculate_sma(losses + [0], period, mpc)

        result = []
        for i in range(len(avg_gain)):
            if avg_loss[i] == 0:
                result.append(100)
            else:
                rs = avg_gain[i] / avg_loss[i]
                rsi = 100 - (100 / (1 + rs))
                result.append(rsi)
        return result
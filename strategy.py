import numpy as np
from enum import Enum

class Signal(Enum):
    NONE = 0
    LONG = 1
    SHORT = 2

class Strategy:
    def __init__(self, settings):
        self.settings = settings

    def ema(self, data, period):
        return np.convolve(data, np.ones(period)/period, mode="valid")

    def signal(self, ohlcv, orderbook):
        closes = np.array([c[4] for c in ohlcv])
        if len(closes) < 50:
            return {"signal": Signal.NONE}

        ema9 = self.ema(closes, 9)
        ema21 = self.ema(closes, 21)

        if ema9[-1] > ema21[-1] and ema9[-2] <= ema21[-2]:
            return {"signal": Signal.LONG, "close": closes[-1], "atr": np.std(closes[-20:])}
        elif ema9[-1] < ema21[-1] and ema9[-2] >= ema21[-2]:
            return {"signal": Signal.SHORT, "close": closes[-1], "atr": np.std(closes[-20:])}

        return {"signal": Signal.NONE}

    def stops(self, sig, close, atr):
        if sig == Signal.LONG:
            return close - 2*atr, close + 3*atr
        elif sig == Signal.SHORT:
            return close + 2*atr, close - 3*atr
        return None, None

import numpy as np
from .config import settings

class Signal:
    NONE = "NONE"
    LONG = "LONG"
    SHORT = "SHORT"

def ema(arr, period):
    arr = np.asarray(arr, dtype=float)
    k = 2 / (period + 1)
    ema_vals = []
    prev = arr[0]
    ema_vals.append(prev)
    for i in range(1, len(arr)):
        prev = arr[i] * k + prev * (1 - k)
        ema_vals.append(prev)
    return np.array(ema_vals)

def atr(high, low, close, period=14):
    trs = [high[0] - low[0]]
    for i in range(1, len(close)):
        tr = max(high[i] - low[i], abs(high[i] - close[i-1]), abs(low[i] - close[i-1]))
        trs.append(tr)
    trs = np.array(trs)
    atr_vals = []
    prev = np.mean(trs[:period])
    atr_vals.extend([np.nan]*(period-1))
    atr_vals.append(prev)
    for i in range(period, len(trs)):
        prev = (prev*(period-1) + trs[i]) / period
        atr_vals.append(prev)
    return np.array(atr_vals)

class Strategy:
    def __init__(self, ob_levels, ob_threshold):
        self.ob_levels = ob_levels
        self.ob_threshold = ob_threshold

    def signal(self, ohlcv, orderbook):
        closes = [c[4] for c in ohlcv]
        highs = [c[2] for c in ohlcv]
        lows = [c[3] for c in ohlcv]

        e9 = ema(closes, 9)
        e21 = ema(closes, 21)
        a14 = atr(highs, lows, closes, 14)

        close = closes[-2]
        e9v, e21v = e9[-2], e21[-2]
        atrv = a14[-2]

        bids = sum([b[1] for b in orderbook["bids"][:self.ob_levels]])
        asks = sum([a[1] for a in orderbook["asks"][:self.ob_levels]])
        obi = bids / (bids + asks) if (bids+asks) > 0 else 0.5

        sig = Signal.NONE
        if e9v > e21v and obi >= self.ob_threshold:
            sig = Signal.LONG
        elif e9v < e21v and obi <= (1 - self.ob_threshold):
            sig = Signal.SHORT

        return {"signal": sig, "close": close, "atr": atrv}
    
    def stops(self, signal, price, atr_val):
        if signal == Signal.LONG:
            sl = price - settings.sl_atr_mult * atr_val
            tp = price + settings.tp_rr * (price - sl)
        else:
            sl = price + settings.sl_atr_mult * atr_val
            tp = price - settings.tp_rr * (sl - price)
        return sl, tp

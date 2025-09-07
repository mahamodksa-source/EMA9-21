import time
from .config import settings
from .exchange import BybitClient
from .strategy import Strategy, Signal
from .utils import CandleGate, now_iso

def main():
    print(f"[{now_iso()}] 🚀 تشغيل البوت (1H EMA9/21 + دفتر الأوامر)")
    ex = BybitClient()
    strat = Strategy(settings.ob_levels, settings.ob_threshold)
    gate = CandleGate()

    while True:
        try:
            ohlcv = ex.fetch_ohlcv(limit=300)
            ob = ex.fetch_orderbook(limit=50)
        except Exception as e:
            print(f"[{now_iso()}] خطأ: {e}")
            time.sleep(settings.poll_seconds)
            continue

        if not gate.update_and_should_run(ohlcv[-1][0]):
            time.sleep(settings.poll_seconds)
            continue

        sig = strat.signal(ohlcv, ob)
        print(f"[{now_iso()}] إشارة: {sig}")

        if sig["signal"] == Signal.NONE:
            time.sleep(settings.poll_seconds)
            continue

        mark = sig["close"]
        sl, tp = strat.stops(sig["signal"], mark, sig["atr"])

        qty = settings.fixed_trade_usdt / mark

        equity = ex.fetch_balance()
        notional = qty * mark
        lev = max(1, min(20, int(notional / equity)))  # يحدد الرافعة بين 1 و 20
        ex.set_leverage(lev)

        side = "buy" if sig["signal"] == Signal.LONG else "sell"

        try:
            order = ex.place_order(side, qty, mark, sl, tp)
            print(f"[{now_iso()}] ✅ تنفيذ الصفقة: {order}")
        except Exception as e:
            print(f"[{now_iso()}] ⚠️ خطأ في تنفيذ الصفقة: {e}")

        time.sleep(settings.poll_seconds)

if __name__ == "__main__":
    main()

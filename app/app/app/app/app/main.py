import time
from datetime import datetime
from config import Settings
from exchange import Exchange
from strategy import Strategy, Signal

def now_iso():
    return datetime.utcnow().isoformat()

def main():
    settings = Settings()
    ex = Exchange(settings)
    strat = Strategy(settings)

    while True:
        try:
            symbols = ex.fetch_all_symbols()
            open_positions = ex.fetch_open_positions()

            if len(open_positions) >= settings.max_open_positions:
                print(f"[{now_iso()}] 🚫 عدد الصفقات المفتوحة وصل الحد ({settings.max_open_positions})")
                time.sleep(settings.poll_seconds)
                continue

            for symbol in symbols:
                try:
                    ohlcv = ex.ex.fetch_ohlcv(symbol, timeframe=settings.timeframe, limit=300)
                    ob = ex.ex.fetch_order_book(symbol, limit=50)
                except Exception as e:
                    print(f"[{now_iso()}] ⚠️ خطأ في {symbol}: {e}")
                    continue

                sig = strat.signal(ohlcv, ob)
                if sig["signal"] == Signal.NONE:
                    continue

                mark = sig["close"]
                sl, tp = strat.stops(sig["signal"], mark, sig["atr"])

                # الكمية بالدولار الثابت
                qty = settings.fixed_trade_usdt / mark
                equity = ex.fetch_balance()
                notional = qty * mark

                lev = max(1, min(20, int(notional / equity)))
                ex.set_leverage(lev, symbol)

                side = "buy" if sig["signal"] == Signal.LONG else "sell"

                try:
                    order = ex.place_order(side, qty, mark, sl, tp, symbol)
                    print(f"[{now_iso()}] ✅ تنفيذ {symbol}: {order}")
                except Exception as e:
                    print(f"[{now_iso()}] ⚠️ خطأ تنفيذ {symbol}: {e}")

            time.sleep(settings.poll_seconds)

        except Exception as e:
            print(f"[{now_iso()}] 🚨 خطأ عام: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()

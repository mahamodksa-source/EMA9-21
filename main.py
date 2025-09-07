from config import Config

print("=== CONFIG DEBUG ===")
print("BYBIT_API_KEY:", Config.BYBIT_API_KEY)
print("BYBIT_API_SECRET:", Config.BYBIT_API_SECRET)
print("BYBIT_NETWORK:", Config.BYBIT_NETWORK)
print("DRY_RUN:", Config.DRY_RUN)
print("FIXED_TRADE_USDT:", Config.FIXED_TRADE_USDT)
print("OB_LEVELS:", Config.OB_LEVELS)
print("OB_THRESHOLD:", Config.OB_THRESHOLD)
print("POLL_SECONDS:", Config.POLL_SECONDS)
print("SL_ATR_MULT:", Config.SL_ATR_MULT)
print("TP_RR:", Config.TP_RR)
print("TELEGRAM_TOKEN:", Config.TELEGRAM_TOKEN)
print("TELEGRAM_CHAT_ID:", Config.TELEGRAM_CHAT_ID)
print("TIMEFRAME:", Config.TIMEFRAME)
print("====================")


import time
from datetime import datetime
from config import Settings
from exchange import Exchange
from strategy import Strategy, Signal
from notifier import Notifier

def now_iso():
    return datetime.utcnow().isoformat()

def main():
    settings = Settings()
    ex = Exchange(settings)
    strat = Strategy(settings)
    notifier = Notifier(settings.telegram_token, settings.telegram_chat_id)

    tracked_orders = {}

    while True:
        try:
            symbols = ex.fetch_all_symbols()
            open_positions = ex.fetch_open_positions()

            # تحقق من الصفقات المغلقة
            for symbol, order in list(tracked_orders.items()):
                still_open = any(p["symbol"] == symbol and float(p["contracts"]) > 0 for p in open_positions)
                if not still_open:
                    entry = order["entryPrice"]
                    side = order["side"]
                    try:
                        closed_price = ex.ex.fetch_ticker(symbol)["last"]
                    except:
                        closed_price = 0

                    pnl = float(order.get("unrealizedPnl", 0))
                    msg = (
                        f"✅ إغلاق صفقة\n"
                        f"العملة: {symbol}\n"
                        f"الاتجاه: {side}\n"
                        f"سعر الدخول: {entry}\n"
                        f"سعر الإغلاق: {closed_price}\n"
                        f"النتيجة: {'ربح ✅' if pnl > 0 else 'خسارة ❌'}\n"
                        f"P&L: {pnl:.2f} USDT"
                    )
                    notifier.send(msg)
                    del tracked_orders[symbol]

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

                qty = settings.fixed_trade_usdt / mark
                equity = ex.fetch_balance()
                notional = qty * mark

                lev = max(1, min(20, int(notional / equity)))
                ex.set_leverage(lev, symbol)

                side = "buy" if sig["signal"] == Signal.LONG else "sell"

                try:
                    order = ex.place_order(side, qty, mark, sl, tp, symbol)
                    print(f"[{now_iso()}] ✅ تنفيذ {symbol}: {order}")

                    msg = (
                        f"🚀 صفقة جديدة\n"
                        f"العملة: {symbol}\n"
                        f"الاتجاه: {'شراء' if sig['signal'].name == 'LONG' else 'بيع'}\n"
                        f"الدخول: {mark}\n"
                        f"وقف الخسارة: {sl}\n"
                        f"جني الأرباح: {tp}\n"
                        f"الرافعة: {lev}x\n"
                        f"القيمة: {settings.fixed_trade_usdt} USDT"
                    )
                    notifier.send(msg)

                    tracked_orders[symbol] = order

                except Exception as e:
                    print(f"[{now_iso()}] ⚠️ خطأ تنفيذ {symbol}: {e}")

            time.sleep(settings.poll_seconds)

        except Exception as e:
            print(f"[{now_iso()}] 🚨 خطأ عام: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()

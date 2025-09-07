import ccxt

class Exchange:
    def __init__(self, settings):
        self.settings = settings
        self.ex = ccxt.bybit({
            "apiKey": settings.api_key,
            "secret": settings.api_secret,
            "enableRateLimit": True,
            "options": {"defaultType": "future"},
        })
        self.ex.set_sandbox_mode(settings.network == "testnet")

    def fetch_all_symbols(self):
        markets = self.ex.load_markets()
        return [s for s in markets if s.endswith("/USDT:USDT")]

    def fetch_balance(self):
        return self.ex.fetch_balance()["total"]["USDT"]

    def fetch_open_positions(self):
        try:
            return self.ex.fetch_positions()
        except Exception:
            return []

    def set_leverage(self, lev, symbol):
        try:
            self.ex.set_leverage(lev, symbol)
        except Exception as e:
            print(f"⚠️ خطأ تحديد الرافعة {symbol}: {e}")

    def place_order(self, side, qty, price, stop_loss, take_profit, symbol):
        params = {"stopLoss": stop_loss, "takeProfit": take_profit}
        return self.ex.create_order(symbol, "market", side, qty, price, params)

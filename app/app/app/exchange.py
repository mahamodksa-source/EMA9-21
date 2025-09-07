import ccxt

class Exchange:
    def __init__(self, settings):
        self.settings = settings
        self.ex = ccxt.bybit({
            "apiKey": settings.api_key,
            "secret": settings.api_secret,
            "enableRateLimit": True,
        })
        if settings.network == "testnet":
            self.ex.set_sandbox_mode(True)

    def fetch_all_symbols(self):
        """جلب كل أزواج USDT Perpetual"""
        markets = self.ex.load_markets()
        symbols = [s for s in markets if ":USDT" in s and markets[s]['type'] == 'swap']
        return symbols

    def fetch_balance(self):
        balance = self.ex.fetch_balance()
        return balance['USDT']['total']

    def set_leverage(self, lev: int, symbol: str):
        try:
            self.ex.set_leverage(lev, symbol=symbol, params={"buyLeverage": lev, "sellLeverage": lev})
        except Exception as e:
            print(f"⚠️ خطأ عند تعيين الرافعة لـ {symbol}: {e}")

    def place_order(self, side: str, qty: float, price: float, sl: float, tp: float, symbol: str):
        params = {
            "stopLoss": sl,
            "takeProfit": tp,
        }
        order = self.ex.create_order(
            symbol=symbol,
            type="market",
            side=side,
            amount=qty,
            params=params
        )
        return order

    def fetch_open_positions(self):
        positions = self.ex.fetch_positions()
        open_pos = [p for p in positions if float(p["contracts"]) > 0]
        return open_pos

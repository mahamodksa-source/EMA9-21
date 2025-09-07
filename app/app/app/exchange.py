import ccxt
from .config import settings

class BybitClient:
    def __init__(self):
        opts = {
            "apiKey": settings.api_key,
            "secret": settings.api_secret,
            "enableRateLimit": True,
            "options": {"defaultType": "swap"},
        }
        if settings.network.lower() == "testnet":
            opts["urls"] = {"api": {"public": "https://api-testnet.bybit.com", "private": "https://api-testnet.bybit.com"}}
        self.ex = ccxt.bybit(opts)
        self.ex.load_markets()

    def fetch_ohlcv(self, limit=200):
        return self.ex.fetch_ohlcv(settings.symbol, timeframe=settings.timeframe, limit=limit)

    def fetch_orderbook(self, limit=50):
        return self.ex.fetch_order_book(settings.symbol, limit=limit)

    def fetch_balance(self) -> float:
        bal = self.ex.fetch_balance(params={"type": "swap"})
        total = bal.get("USDT", {}).get("total")
        if total is None:
            total = bal.get("USDT", {}).get("free", 0.0)
        return float(total)

    def set_leverage(self, lev: int):
        try:
            self.ex.set_leverage(lev, settings.symbol)
        except Exception:
            pass

    def place_order(self, side: str, qty: float, price: float, sl: float, tp: float):
        if settings.dry_run:
            return {"side": side, "qty": qty, "entry": price, "sl": sl, "tp": tp, "dry_run": True}
        return self.ex.create_order(symbol=settings.symbol, type="limit", side=side, amount=qty, price=price)

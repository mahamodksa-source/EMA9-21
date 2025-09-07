import os

class Settings:
    def __init__(self):
        self.api_key = os.getenv("BYBIT_API_KEY")
        self.api_secret = os.getenv("BYBIT_API_SECRET")
        self.network = os.getenv("BYBIT_NETWORK", "testnet")
        self.fixed_trade_usdt = float(os.getenv("FIXED_TRADE_USDT", 100))
        self.timeframe = "1h"
        self.max_open_positions = 3
        self.poll_seconds = 30
        self.telegram_token = os.getenv("TELEGRAM_TOKEN")
        self.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

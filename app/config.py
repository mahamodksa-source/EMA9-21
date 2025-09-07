import os
from dataclasses import dataclass

@dataclass
class Settings:
    api_key: str = os.getenv("BYBIT_API_KEY", "")
    api_secret: str = os.getenv("BYBIT_API_SECRET", "")
    symbol: str = os.getenv("SYMBOL", "BTC/USDT:USDT")
    timeframe: str = os.getenv("TIMEFRAME", "1h")
    fixed_trade_usdt: float = float(os.getenv("FIXED_TRADE_USDT", "100"))  # قيمة الصفقة الثابتة
    sl_atr_mult: float = float(os.getenv("SL_ATR_MULT", "1.5"))
    tp_rr: float = float(os.getenv("TP_RR", "2.0"))
    ob_levels: int = int(os.getenv("OB_LEVELS", "5"))
    ob_threshold: float = float(os.getenv("OB_THRESHOLD", "0.60"))
    poll_seconds: int = int(os.getenv("POLL_SECONDS", "55"))
    dry_run: bool = os.getenv("DRY_RUN", "false").lower() == "true"
    network: str = os.getenv("BYBIT_NETWORK", "mainnet")

settings = Settings()

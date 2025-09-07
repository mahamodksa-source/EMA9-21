import os
from dataclasses import dataclass

@dataclass
class Settings:
    api_key: str = os.getenv("BYBIT_API_KEY", "")
    api_secret: str = os.getenv("BYBIT_API_SECRET", "")
    timeframe: str = os.getenv("TIMEFRAME", "1h")
    fixed_trade_usdt: float = float(os.getenv("FIXED_TRADE_USDT", "100"))  # المبلغ الثابت لكل صفقة
    sl_atr_mult: float = float(os.getenv("SL_ATR_MULT", "1.5"))           # مضاعف ATR لوقف الخسارة
    tp_rr: float = float(os.getenv("TP_RR", "2.0"))                       # نسبة الهدف (RR)
    ob_levels: int = int(os.getenv("OB_LEVELS", "5"))                     # عمق دفتر الأوامر
    ob_threshold: float = float(os.getenv("OB_THRESHOLD", "0.60"))        # نسبة انحياز دفتر الأوامر
    max_pos_usdt: float = float(os.getenv("MAX_POS_USDT", "200"))         # أقصى قيمة للصفقة
    min_notional: float = float(os.getenv("MIN_NOTIONAL", "10"))          # أقل قيمة للصفقة
    max_open_positions: int = int(os.getenv("MAX_OPEN_POSITIONS", "5"))   # أقصى عدد صفقات مفتوحة
    poll_seconds: int = int(os.getenv("POLL_SECONDS", "55"))              # وقت الانتظار بين كل دورة
    dry_run: bool = os.getenv("DRY_RUN", "false").lower() == "true"
    network: str = os.getenv("BYBIT_NETWORK", "mainnet")                  # mainnet أو testnet

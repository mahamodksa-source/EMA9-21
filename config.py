import os

class Config:
    # Bybit API
    BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
    BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")
    BYBIT_NETWORK = os.getenv("BYBIT_NETWORK", "mainnet")  # mainnet أو testnet

    # التشغيل التجريبي (بدون تنفيذ أوامر حقيقية)
    DRY_RUN = os.getenv("DRY_RUN", "False").lower() == "true"

    # حجم الصفقة الثابتة
    FIXED_TRADE_USDT = float(os.getenv("FIXED_TRADE_USDT", 10))

    # مستويات الـ Order Block
    OB_LEVELS = int(os.getenv("OB_LEVELS", 3))
    OB_THRESHOLD = float(os.getenv("OB_THRESHOLD", 0.5))

    # إعدادات البوت
    POLL_SECONDS = int(os.getenv("POLL_SECONDS", 30))  # عدد الثواني بين كل فحص
    SL_ATR_MULT = float(os.getenv("SL_ATR_MULT", 1.5))  # مضاعف ATR لحساب Stop Loss
    TP_RR = float(os.getenv("TP_RR", 2.0))  # الهدف = نسبة المخاطرة للعائد

    # تيليجرام
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    # الإطار الزمني للتحليل (مثال: 1m, 5m, 15m, 1h, 4h, 1d)
    TIMEFRAME = os.getenv("TIMEFRAME", "15m")

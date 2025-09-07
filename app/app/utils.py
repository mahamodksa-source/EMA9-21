

class CandleGate:
    """لكشف إغلاق شمعة جديدة (مثلاً 1H)."""
    def __init__(self):
        self.last_closed_ts = None
    def update_and_should_run(self, last_candle_ts_ms: int) -> bool:
        if self.last_closed_ts is None:
            self.last_closed_ts = last_candle_ts_ms
            return True
        if last_candle_ts_ms > self.last_closed_ts:
            self.last_closed_ts = last_candle_ts_ms
            return True
        return False

def now_iso():
    return datetime.now(timezone.utc).isoformat()

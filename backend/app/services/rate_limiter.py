import asyncio
import time


class RateLimiter:
    """Simple in-memory rate limiter.

    This is a placeholder for a production-grade solution like Redis or an API gateway.
    """

    def __init__(self, max_requests: int = 30, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._lock = asyncio.Lock()
        self._requests = []  # stores timestamps

    async def allow(self) -> bool:
        now = time.time()
        window_start = now - self.window_seconds
        async with self._lock:
            self._requests = [t for t in self._requests if t >= window_start]
            if len(self._requests) >= self.max_requests:
                return False
            self._requests.append(now)
            return True

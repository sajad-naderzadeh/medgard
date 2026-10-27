import time
from collections import defaultdict, deque


class RateLimiter:
    def __init__(
        self,
        max_requests: int = 60,
        window_seconds: int = 60,
    ):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(deque)

    def is_allowed(self, client_id: str) -> bool:
        now = time.time()
        queue = self.requests[client_id]

        while queue and now - queue[0] >= self.window_seconds:
            queue.popleft()

        if len(queue) >= self.max_requests:
            return False

        queue.append(now)
        return True

from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Dict


class PresenceService:

    def __init__(self) -> None:
        self._connection_counts: Dict[str, int] = defaultdict(int)
        self._last_seen: Dict[str, datetime] = {}

    def set_online(self, user_id: str) -> None:
        self._connection_counts[user_id] += 1

    def set_offline(self, user_id: str) -> None:
        current = self._connection_counts.get(user_id, 0)
        if current <= 1:
            self._connection_counts.pop(user_id, None)
            self._last_seen[user_id] = datetime.utcnow()
        else:
            self._connection_counts[user_id] = current - 1

    def is_online(self, user_id: str) -> bool:
        return self._connection_counts.get(user_id, 0) > 0

    def last_seen(self, user_id: str) -> datetime | None:
        return self._last_seen.get(user_id)


presence_service = PresenceService()

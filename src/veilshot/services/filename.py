from __future__ import annotations

from datetime import datetime


def screenshot_filename(now: datetime | None = None) -> str:
    current = now or datetime.now()
    return current.strftime("Screenshot_%Y-%m-%d_%H-%M-%S.png")

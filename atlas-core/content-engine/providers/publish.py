from __future__ import annotations

from typing import List

from .base import Provider


_CHECKLIST = [
    "Review and approve final script",
    "Render or export all media assets",
    "Generate thumbnails",
    "Write platform-specific descriptions",
    "Schedule publish date and time",
    "Verify all links and references",
    "Confirm brand guidelines are met",
    "Prepare analytics tracking links",
    "Post to all target channels",
    "Monitor initial engagement",
]


class PublishProvider(Provider):
    """Deterministic publishing checklist provider.

    Returns a fixed checklist of publishing tasks.
    No AI required.
    """

    def generate(self, idea: str) -> List[str]:
        return _CHECKLIST[:]

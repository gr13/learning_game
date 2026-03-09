from __future__ import annotations

from app.lessons.adapters.base import BaseLessonAdapter
from app.lessons.adapters.core import CoreLessonAdapter


class LessonRegistry:
    """Adapter registry for module-specific lesson logic."""

    def __init__(self) -> None:
        self._adapters: dict[int, BaseLessonAdapter] = {
            1: CoreLessonAdapter(),
        }

    def get_adapter(self, module_id: int) -> BaseLessonAdapter | None:
        return self._adapters.get(module_id)

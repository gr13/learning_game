from __future__ import annotations

from app.lessons.adapters.base import BaseLessonAdapter
from app.lessons.adapters.core import CoreLessonAdapter


class LessonRegistry:
    """Adapter registry for module-specific lesson logic."""

    def __init__(self) -> None:
        self._adapters_by_type: dict[int, BaseLessonAdapter] = {
            1: CoreLessonAdapter(1, "core", 5),
            2: CoreLessonAdapter(2, "domain", 5),
            3: CoreLessonAdapter(3, "reading", 1),
            4: CoreLessonAdapter(4, "writing", 1),
            5: CoreLessonAdapter(5, "speaking", 1),
        }

    def get_adapter(self, module_type_id: int) -> BaseLessonAdapter | None:
        return self._adapters_by_type.get(module_type_id)

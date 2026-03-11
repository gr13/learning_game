from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from app.lessons.contracts import LessonEvent, LessonState


class BaseLessonAdapter(ABC):
    """Module adapter interface for lesson orchestration."""

    module_type_id: int
    plan_module_name: str
    max_exercises: int

    @abstractmethod
    def build_start_package(self, state: LessonState) -> dict[str, Any]:
        """Build initial package sent to ChatGPT for GET/start."""
        pass

    @abstractmethod
    def build_continue_package(
        self,
        state: LessonState,
        event: LessonEvent,
    ) -> dict[str, Any]:
        """Build continuation package sent to ChatGPT for POST/continue."""
        pass

    @abstractmethod
    def expected_schema_for_phase(
        self,
        state: LessonState,
    ) -> dict[str, Any] | None:
        """Return schema expected from ChatGPT for current phase."""
        pass

    @abstractmethod
    def parse_reply(self, raw_reply: str) -> dict[str, Any] | str:
        """Parse ChatGPT raw reply into structured payload or text."""
        pass

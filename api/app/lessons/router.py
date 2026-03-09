from __future__ import annotations

from typing import Any

from app.lessons.orchestrator import LessonOrchestrator


class LessonRouter:
    """Module-level lesson router for GET/POST lesson calls."""

    def __init__(self) -> None:
        self.orchestrator = LessonOrchestrator()

    def handle_get(self, module_id: int, session_id: int) -> dict[str, Any]:
        return self.orchestrator.start(module_id, session_id)

    def handle_post(
        self,
        module_id: int,
        session_id: int,
        user_input: str,
    ) -> dict[str, Any]:
        return self.orchestrator.continue_turn(
            module_id,
            session_id,
            user_input,
        )

from __future__ import annotations

from typing import Any

from app.lessons.orchestrator import LessonOrchestrator
from app.models.modules import ModulesModel
from app.models.sessions import SessionsModel


class LessonEngine:
    """Compatibility engine for resources/module.py.

    This mirrors the existing `ModuleEngine.run_module(...)` signature so
    `resources/module.py` can switch engines with minimal changes.
    """

    def __init__(self) -> None:
        self.orchestrator = LessonOrchestrator()

    def run_module(
        self,
        module: ModulesModel,
        session: SessionsModel,
        user_input: str | None = None,
    ) -> dict[str, Any]:
        if user_input is None:
            return self.orchestrator.start(
                module_id=module.id,
                session_id=session.id,
            )

        return self.orchestrator.continue_turn(
            module_id=module.id,
            session_id=session.id,
            user_input=user_input,
        )

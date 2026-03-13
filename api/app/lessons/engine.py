from __future__ import annotations

from typing import Any

from app.lessons.orchestrator import LessonOrchestrator
from app.models.modules import ModulesModel
from app.models.sessions import SessionsModel
from app.models.exercises import ExercisesModel


class LessonEngine:
    def __init__(self) -> None:
        self.orchestrator = LessonOrchestrator()

    def start(
        self,
        module_type_id: int,
        module: ModulesModel,
        session: SessionsModel,
        exercise: ExercisesModel,
    ) -> dict[str, Any]:
        return self.orchestrator.start(
            module_type_id=module_type_id,
            module=module,
            session=session,
            exercise=exercise,
        )

    def answer(
        self,
        module_type_id: int,
        module: ModulesModel,
        session: SessionsModel,
        user_input: str,
    ) -> dict[str, Any]:
        return self.orchestrator.continue_turn(
            module_type_id=module_type_id,
            module_id=module.id,
            session_id=session.id,
            user_input=user_input,
        )

    def next_exercise(
        self,
        module_type_id: int,
        module: ModulesModel,
        session: SessionsModel,
    ) -> dict[str, Any]:
        return self.orchestrator.next_exercise(
            module_type_id=module_type_id,
            module_id=module.id,
            session_id=session.id,
        )

    def end_module(
        self,
        module_type_id: int,
        module: ModulesModel,
        session: SessionsModel,
    ) -> dict[str, Any]:
        return self.orchestrator.end_module(
            module_type_id=module_type_id,
            module_id=module.id,
            session_id=session.id,
        )

from __future__ import annotations

import json
from typing import Any

from app.lessons.adapters.base import BaseLessonAdapter
from app.lessons.contracts import LessonEvent, LessonState
from app.lessons.plan_loader import load_plan_bundle
from app.lessons.schemas import LESSON_JSON_SCHEMA
from app.models.profile import ProfileModel


class CoreLessonAdapter(BaseLessonAdapter):
    """Generic plan-based adapter for CORE/DOMAIN/READING/WRITING/SPEAKING."""

    def __init__(
        self,
        module_type_id: int,
        plan_module_name: str,
        max_exercises: int,
    ) -> None:
        self.module_type_id = module_type_id
        self.plan_module_name = plan_module_name
        self.max_exercises = max_exercises

    def build_start_package(self, state: LessonState) -> dict[str, Any]:
        plans = load_plan_bundle(module_name=self.plan_module_name)
        profile = ProfileModel.find_by_id(1)

        return {
            "plans": plans,
            "runtime": {
                "session_id": state.session_id,
                "practice_level": (
                    profile.get_user_level() if profile else "A2"
                ),
                "exercise_index": state.exercise_index,
                "phase": state.phase.value,
                "max_exercises": self.max_exercises,
            },
            "intent": "start_module",
        }

    def build_continue_package(
        self,
        state: LessonState,
        event: LessonEvent,
    ) -> dict[str, Any]:
        return {
            "runtime": {
                "session_id": state.session_id,
                "exercise_index": state.exercise_index,
                "phase": state.phase.value,
                "max_exercises": self.max_exercises,
            },
            "event": {
                "type": event.event_type.value,
                "user_input": event.user_input,
            },
            "intent": event.event_type.value,
        }

    def expected_schema_for_phase(
        self,
        _state: LessonState,
    ) -> dict[str, Any] | None:
        return LESSON_JSON_SCHEMA

    def parse_reply(self, raw_reply: str) -> dict[str, Any] | str:
        try:
            return json.loads(raw_reply)
        except json.JSONDecodeError:
            return raw_reply

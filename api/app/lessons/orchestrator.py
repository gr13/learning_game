from __future__ import annotations

import json
from typing import Any

from app.lessons.chat_loop import ChatLoopService
from app.lessons.contracts import (
    EventType,
    LessonEnvelope,
    LessonEvent,
    LessonState,
)
from app.lessons.registry import LessonRegistry
from app.lessons.state_machine import LessonStateMachine
from app.sessions.session_store import SessionStore


class LessonOrchestrator:
    """High-level GET/POST lesson orchestration skeleton."""

    def __init__(self) -> None:
        self.registry = LessonRegistry()
        self.state_machine = LessonStateMachine()
        self.chat_loop = ChatLoopService()

    def start(self, module_id: int, session_id: int) -> LessonEnvelope:
        adapter = self.registry.get_adapter(module_id)
        if not adapter:
            return {
                "mode": "error",
                "message": f"Module {module_id} not implemented.",
            }

        state = LessonState(module_id=module_id, session_id=session_id)
        state = self.state_machine.apply(state, LessonEvent(EventType.START))

        package = adapter.build_start_package(state)
        system_prompt = self._build_system_prompt(package)

        SessionStore.append_message(session_id, "system", system_prompt)
        SessionStore.append_message(session_id, "user", "show the new word")

        return self.chat_loop.call(
            session_id=session_id,
            expected_schema=adapter.expected_schema_for_phase(state),
            expect_json=True,
        )

    def continue_turn(
        self,
        module_id: int,
        session_id: int,
        user_input: str,
    ) -> LessonEnvelope:
        adapter = self.registry.get_adapter(module_id)
        if not adapter:
            return {
                "mode": "error",
                "message": f"Module {module_id} not implemented.",
            }

        if not user_input.strip():
            return {
                "mode": "error",
                "message": "User input cannot be empty.",
            }

        state = LessonState(module_id=module_id, session_id=session_id)
        event = LessonEvent(EventType.USER_ANSWER, user_input=user_input)
        state = self.state_machine.apply(state, event)

        package = adapter.build_continue_package(state, event)
        SessionStore.append_message(
            session_id,
            "system",
            self._build_system_prompt(package),
        )
        SessionStore.append_message(session_id, "user", user_input)

        return self.chat_loop.call(
            session_id=session_id,
            expected_schema=adapter.expected_schema_for_phase(state),
            expect_json=None,
        )

    @staticmethod
    def _build_system_prompt(package: dict[str, Any]) -> str:
        return (
            "You are a German language teacher. "
            "Follow the package exactly. "
            "Return JSON when structured response is required.\n\n"
            f"Package:\n{json.dumps(package, ensure_ascii=True, indent=2)}"
        )

from __future__ import annotations

import json
from typing import Any

from app.api_helpers.schemas import EXPLANATION_SCHEMA
from app.lessons.chat_loop import ChatLoopService
from app.lessons.contracts import (
    EventType,
    LessonEnvelope,
    LessonEvent,
    LessonState,
    Phase,
)


from app.lessons.registry import LessonRegistry
from app.lessons.schemas import EXERCISE_SCHEMA
from app.lessons.state_machine import LessonStateMachine
from app.sessions.session_store import SessionStore
from app.models.core_vocabulary import CoreVocabularyModel


class LessonOrchestrator:
    def __init__(self) -> None:
        self.registry = LessonRegistry()
        self.state_machine = LessonStateMachine()
        self.chat_loop = ChatLoopService()

    def start(
            self, module_type_id: int, module_id: int, session_id: int
            ) -> LessonEnvelope:
        adapter = self.registry.get_adapter(module_type_id)
        if not adapter:
            return {"mode": "error", "message": f"Module type {module_type_id} not implemented."}  # noqa: E501

        state = LessonState(
            module_type_id=module_type_id,
            session_id=session_id
        )
        state = self.state_machine.apply(state, LessonEvent(EventType.START))
        state.exercise_index = 1

        if module_type_id == 1:
            row = CoreVocabularyModel.find_new()
            if not row:
                return {
                    "mode": "error",
                    "message": "No new core vocabulary word found.",
                }

            row.mark_introduced()
            introduced_words = [
                w.word for w in CoreVocabularyModel.find_introduced()]

            state.metadata["the_new_word"] = row.word
            state.metadata["practice_list"] = introduced_words

        package = adapter.build_start_package(state)
        SessionStore.append_message(
            session_id,
            "system",
            self._build_system_prompt(package)
        )

        seed_word = state.metadata.get("the_new_word")
        if seed_word:
            SessionStore.append_message(
                session_id,
                "user",
                f"Introduce this exact word: {seed_word}",
            )
        else:
            SessionStore.append_message(
                session_id,
                "user",
                "Introduce one new word.",
            )

        explanation = self.chat_loop.call(session_id, EXPLANATION_SCHEMA, True)
        if explanation["mode"] != "json":
            return explanation

        SessionStore.append_message(
            session_id,
            "system",
            "Now generate Exercise 1 only. Return mode='exercise' JSON.",
        )
        SessionStore.append_message(session_id, "user", "Start exercise 1.")
        exercise = self.chat_loop.call(session_id, EXERCISE_SCHEMA, True)
        if exercise["mode"] != "json":
            return exercise

        SessionStore.create_exercise_marker(session_id, module_id, 1)

        return {
            "mode": "json",
            "message": [explanation["message"], exercise["message"]]
        }

    def continue_turn(
        self,
        module_type_id: int,
        module_id: int,
        session_id: int,
        user_input: str,
    ) -> LessonEnvelope:
        adapter = self.registry.get_adapter(module_type_id)
        if not adapter:
            return {
                "mode": "error", "message": f"Module type {module_type_id} not implemented."  # noqa: E501
            }
        if not user_input.strip():
            return {
                "mode": "error", "message": "User input cannot be empty."
            }

        current_ex = SessionStore.get_current_exercise_index(
            session_id, module_id)
        state = LessonState(
            module_type_id=module_type_id,
            session_id=session_id,
            exercise_index=max(1, current_ex),
        )

        event = LessonEvent(EventType.USER_ANSWER, user_input=user_input)
        state = self.state_machine.apply(state, event)

        package = adapter.build_continue_package(state, event)
        SessionStore.append_message(
            session_id, "system", self._build_system_prompt(package))
        SessionStore.append_message(session_id, "user", user_input)

        return self.chat_loop.call(
            session_id, expected_schema=None, expect_json=None)

    def next_exercise(
            self, module_type_id: int, module_id: int, session_id: int
            ) -> LessonEnvelope:
        adapter = self.registry.get_adapter(module_type_id)
        if not adapter:
            return {
                "mode": "error", "message": f"Module type {module_type_id} not implemented."  # noqa: E501
            }

        current_ex = SessionStore.get_current_exercise_index(
            session_id, module_id)
        if current_ex >= adapter.max_exercises:
            return {
                "mode": "error",
                "message": "No more exercises. Press End Module.",
            }

        state = LessonState(
            module_type_id=module_type_id,
            session_id=session_id,
            phase=Phase.EXERCISE,
            exercise_index=current_ex,
        )
        state = self.state_machine.apply(
            state, LessonEvent(EventType.NEXT_EXERCISE))

        if module_type_id == 1:
            state.metadata["practice_list"] = [
                w.word for w in CoreVocabularyModel.find_introduced()
            ]

        package = adapter.build_continue_package(state, LessonEvent(
            EventType.NEXT_EXERCISE))
        SessionStore.append_message(
            session_id, "system", self._build_system_prompt(package))
        SessionStore.append_message(
            session_id,
            "user",
            f"Start exercise {state.exercise_index}. Return mode='exercise' JSON.",  # noqa: E501
        )

        exercise = self.chat_loop.call(session_id, EXERCISE_SCHEMA, True)
        if exercise["mode"] != "json":
            return exercise

        SessionStore.create_exercise_marker(
            session_id, module_id, state.exercise_index)
        return exercise

    def end_module(
            self, module_type_id: int, module_id: int, session_id: int
            ) -> LessonEnvelope:
        _ = module_type_id, module_id
        messages = SessionStore.get_messages(session_id)
        transcript = "\n".join(
            f"{m.role}: {m.content}" for m in messages
        )

        SessionStore.append_message(
            session_id,
            "system",
            (
                "Analyze full transcript and return plain text with 3 sections:\n"  # noqa: E501
                "1) Introduced words\n"
                "2) Learned words\n"
                "3) Teacher status"
            ),
        )
        SessionStore.append_message(
            session_id,
            "user",
            f"Session transcript:\n{transcript}",
        )

        return self.chat_loop.call(
            session_id, expected_schema=None, expect_json=False)

    @staticmethod
    def _build_system_prompt(package: dict[str, Any]) -> str:
        return (
            "You are a German language teacher. Follow the package exactly. "
            "Return JSON when structured response is required.\n\n"
            f"Package:\n{json.dumps(package, ensure_ascii=True, indent=2)}"
        )

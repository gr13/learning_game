from __future__ import annotations

import json
from typing import Any

from app.ai.chatgpt import ChatGPT
from app.api_helpers.response_handler import ResponseHandler
from app.api_helpers.schemas import EXPLANATION_SCHEMA
from app.lessons.plan_loader import load_plan_bundle
from app.models.profile import ProfileModel
from app.sessions.session_store import SessionStore


class CoreLessonService:
    """Straight-through CORE lesson cycle.

    GET path:
    - build package from plan JSON files + runtime context
    - append system/user bootstrap messages
    - call ChatGPT
    - persist assistant reply
    - return normalized envelope for UI

    POST path:
    - append user reply
    - ensure exercise mode prompt
    - call ChatGPT with full history
    - persist assistant reply
    - return normalized envelope for UI
    """

    MAX_RETRIES = 2

    def __init__(self) -> None:
        self.chat = ChatGPT()

    def handle_get(self, session_id: int) -> dict[str, Any]:
        plan_bundle = load_plan_bundle()
        profile = ProfileModel.find_by_id(1)

        runtime = {
            "practice_level": profile.get_user_level() if profile else "A2",
            "session_id": session_id,
        }

        system_payload = {
            "plans": plan_bundle,
            "runtime": runtime,
            "task": "introduce new word and prepare first exercise",
        }

        system_prompt = self._build_system_prompt(system_payload)
        user_prompt = "show the new word"

        SessionStore.append_message(session_id, "system", system_prompt)
        SessionStore.append_message(session_id, "user", user_prompt)

        return self._guarded_call(
            session_id=session_id,
            expected_schema=EXPLANATION_SCHEMA,
            expect_json=True,
        )

    def handle_post(self, session_id: int, user_input: str) -> dict[str, Any]:
        if not user_input.strip():
            return {
                "mode": "error",
                "message": "User input cannot be empty.",
            }

        SessionStore.append_message(session_id, "user", user_input)

        SessionStore.ensure_exercise_mode(
            session_id,
            (
                "Now continue the exercise. "
                "Return JSON for structured tasks and plain text "
                "for teacher feedback."
            ),
        )

        return self._guarded_call(
            session_id=session_id,
            expected_schema=None,
            expect_json=None,
        )

    def _guarded_call(
        self,
        session_id: int,
        expected_schema: dict[str, Any] | None,
        expect_json: bool | None,
    ) -> dict[str, Any]:
        for _ in range(self.MAX_RETRIES):
            messages = self._to_openai_messages(
                SessionStore.get_messages(session_id)
            )
            response = self.chat.send_messages(messages)
            assistant_reply = response.choices[0].message.content or ""

            if not assistant_reply:
                continue

            is_json = ResponseHandler.is_json(assistant_reply)

            if expect_json is True and not is_json:
                self._inject_retry_instruction(session_id)
                continue

            if is_json:
                if expected_schema and not ResponseHandler.validate_json(
                    assistant_reply, expected_schema
                ):
                    self._inject_retry_instruction(session_id)
                    continue

                parsed = json.loads(assistant_reply)
                SessionStore.append_message(
                    session_id,
                    "assistant",
                    assistant_reply,
                )
                return {
                    "mode": "json",
                    "message": parsed,
                }

            SessionStore.append_message(
                session_id,
                "assistant",
                assistant_reply,
            )
            return {
                "mode": "text",
                "message": assistant_reply,
            }

        return {
            "mode": "error",
            "message": "Invalid structured response after retries.",
        }

    @staticmethod
    def _to_openai_messages(messages: list[Any]) -> list[dict[str, str]]:
        normalized: list[dict[str, str]] = []

        for message in messages:
            role = getattr(message, "role", "system")
            content = getattr(message, "content", "")

            # OpenAI roles supported for chat.completions
            if role not in {"system", "user", "assistant"}:
                role = "system"

            normalized.append({
                "role": role,
                "content": content,
            })

        return normalized

    @staticmethod
    def _build_system_prompt(payload: dict[str, Any]) -> str:
        return (
            "You are a German language teacher. "
            "Strictly follow the provided lesson package. "
            "For structured outputs return valid JSON only.\n\n"
            "Lesson package:\n"
            f"{json.dumps(payload, ensure_ascii=True, indent=2)}"
        )

    @staticmethod
    def _inject_retry_instruction(session_id: int) -> None:
        SessionStore.append_message(
            session_id,
            "system",
            (
                "Your previous response was invalid. "
                "Return ONLY valid JSON matching the expected schema."
            ),
        )

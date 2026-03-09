from __future__ import annotations

import json
from typing import Any

from app.ai.chatgpt import ChatGPT
from app.api_helpers.response_handler import ResponseHandler
from app.lessons.contracts import LessonEnvelope, ResponseMode
from app.sessions.session_store import SessionStore


class ChatLoopService:
    """Continuous ChatGPT request/reply loop using session history."""

    def __init__(self, retries: int = 2) -> None:
        self.chat = ChatGPT()
        self.retries = retries

    def call(
        self,
        session_id: int,
        expected_schema: dict[str, Any] | None,
        expect_json: bool | None,
    ) -> LessonEnvelope:
        for _ in range(self.retries):
            messages = self._to_openai_messages(
                SessionStore.get_messages(session_id))
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
                    session_id, "assistant", assistant_reply)
                return {
                    "mode": ResponseMode.JSON.value,
                    "message": parsed,
                }

            SessionStore.append_message(
                session_id, "assistant", assistant_reply)
            return {
                "mode": ResponseMode.TEXT.value,
                "message": assistant_reply,
            }

        return {
            "mode": ResponseMode.ERROR.value,
            "message": "Invalid structured response after retries.",
        }

    @staticmethod
    def _to_openai_messages(messages: list[Any]) -> list[dict[str, str]]:
        normalized: list[dict[str, str]] = []

        for message in messages:
            role = getattr(message, "role", "system")
            content = getattr(message, "content", "")

            if role not in {"system", "user", "assistant"}:
                role = "system"

            normalized.append({"role": role, "content": content})

        return normalized

    @staticmethod
    def _inject_retry_instruction(session_id: int) -> None:
        SessionStore.append_message(
            session_id,
            "system",
            (
                "Your previous response was invalid. "
                "Return ONLY valid JSON matching the required schema."
            ),
        )

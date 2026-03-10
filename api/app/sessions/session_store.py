from typing import List

from app.models.sessions import SessionsModel
from app.models.session_messages import SessionMessagesModel


class SessionStore:
    """
    Session persistence layer.

    Wraps database models for session handling.
    """

    # -------------------------------------------------------
    # Session creation
    # -------------------------------------------------------

    @staticmethod
    def create_session(module_id: int = None) -> SessionsModel:

        session = SessionsModel(module_id=module_id)

        session.save_to_db()

        return session

    # -------------------------------------------------------
    # Session retrieval
    # -------------------------------------------------------

    @staticmethod
    def get_session(session_id: int) -> SessionsModel | None:

        return SessionsModel.find_by_id(session_id)

    # -------------------------------------------------------
    # Message append
    # -------------------------------------------------------

    @staticmethod
    def append_message(
        session_id: int,
        role: str,
        content: str,
        exercise: int = 1,
    ) -> SessionMessagesModel:

        message = SessionMessagesModel(
            session_id=session_id,
            role=role,
            content=content,
            current_exercise=exercise,
        )

        message.save_to_db()

        return message

    # -------------------------------------------------------
    # Message history
    # -------------------------------------------------------

    @staticmethod
    def get_messages(session_id: int) -> List[SessionMessagesModel]:

        return SessionMessagesModel.find_by_session(session_id)

    # -------------------------------------------------------
    # Exercise mode helper
    # -------------------------------------------------------

    @staticmethod
    def ensure_exercise_mode(session_id: int, system_prompt: str) -> None:

        messages = SessionMessagesModel.find_by_session(session_id)

        already_set = any(
            m.role == "system"
            and "Now continue the exercise" in m.content
            for m in messages
        )

        if not already_set:
            SessionStore.append_message(
                session_id=session_id,
                role="system",
                content=system_prompt,
            )

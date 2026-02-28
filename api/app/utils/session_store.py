import uuid
# ============================================================
# IN-MEMORY SESSION STORE (TEMPORARY)
# ============================================================

# Structure:
# {
#   session_id: {
#       "module": int,
#       "messages": list
#   }
# }


class SessionStore:
    """
    In-memory session storage (temporary).
    Class-based design.
    Shared across entire application.
    """
    _sessions = {}

    @classmethod
    def create_session(cls, module_id: int):
        """
        Creates a new session and returns session_id.
        """
        session_id = str(uuid.uuid4())

        cls._sessions[session_id] = {
            "module": module_id,
            "messages": []
        }

        return session_id

    @classmethod
    def append_message(cls, session_id, role, content):
        """
        Appends a message to session history.
        """
        cls._sessions[session_id]["messages"].append(
            {
                "role": role,
                "content": content
            }
        )

    @classmethod
    def get_messages(cls, session_id):
        """
        Returns message list for given session.
        """
        return cls._sessions[session_id]["messages"]

    @classmethod
    def has_session(cls, session_id):
        """
        Optional safety check.
        """
        return session_id in cls._sessions

    @staticmethod
    def ensure_exercise_mode(
            session_id: int,
            system_prompt: str
                             ) -> None:
        """
        Ensures that the exercise-mode system instruction
        is added only once to the session.
        """

        messages = SessionStore.get_messages(session_id)

        already_set = any(
            (
                m["role"] == "system"
                and "Now continue the exercise" in m["content"]
            )
            for m in messages
        )

        if not already_set:
            SessionStore.append_message(
                session_id,
                "system",
                system_prompt,
            )

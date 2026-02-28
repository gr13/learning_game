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

SESSIONS = {}


class SessionStore:
    @staticmethod
    def create_session(module_id: int):

        session_id = str(uuid.uuid4())

        SESSIONS[session_id] = {
            "module": module_id,
            "messages": []
        }

        return session_id

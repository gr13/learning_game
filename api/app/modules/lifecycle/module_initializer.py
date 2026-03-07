import uuid
from typing import Dict, Any

from app.models.modules import ModulesModel
from app.models.sessions import SessionsModel
from app.models.profile import ProfileModel


class ModuleInitializer:
    """
    Prepare module execution environment.
    """

    def __init__(self, module: ModulesModel):
        self.module = module

    # -------------------------------------------------------
    # Public API
    # -------------------------------------------------------
    def initialize(self) -> SessionsModel:
        """
        Initialize module session.
        """

        session = self.get_existing_session()

        if session:
            return session

        return self.create_session()

    # -------------------------------------------------------
    # Session lookup
    # -------------------------------------------------------
    def get_existing_session(self) -> SessionsModel | None:
        """
        Return latest session for module if exists.
        """

        sessions = SessionsModel.find_by_module_id(self.module.id)

        if not sessions:
            return None

        return sessions[-1]

    # -------------------------------------------------------
    # Session creation
    # -------------------------------------------------------
    def create_session(self) -> SessionsModel:
        """
        Create new module session.
        """

        session = SessionsModel(
            module_id=self.module.id,
            session_id=str(uuid.uuid4())
        )

        session.save_to_db()

        return session

    # -------------------------------------------------------
    # User context
    # -------------------------------------------------------
    def get_user_level(self):
        """
        Retrieve user practice level.
        """

        profile = ProfileModel.find_by_id(1)

        if profile:
            return profile.get_user_level()

        return None

    # -------------------------------------------------------
    # Initialization payload
    # -------------------------------------------------------
    def build_context(self) -> Dict[str, Any]:
        """
        Build initialization context for module.
        """

        return {
            "module_id": self.module.id,
            "module_type": self.module.module_type.value,
            "practice_level": self.get_user_level(),
        }

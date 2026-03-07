from typing import Dict, Any

from app.models.modules import ModulesModel
from app.models.sessions import SessionsModel


class ModuleFinalizer:
    """
    Handles module completion logic.
    """

    def __init__(self, module: ModulesModel, session: SessionsModel):
        self.module = module
        self.session = session

    # -------------------------------------------------------
    # Public API
    # -------------------------------------------------------
    def finalize(self) -> Dict[str, Any]:
        """
        Finalize module execution.
        """

        self.mark_module_done()

        self.finalize_session()

        return self.build_response()

    # -------------------------------------------------------
    # Module state
    # -------------------------------------------------------
    def mark_module_done(self) -> None:
        """
        Mark module as completed.
        """

        if not self.module.done:
            self.module.mark_done()

    # -------------------------------------------------------
    # Session state
    # -------------------------------------------------------
    def finalize_session(self) -> None:
        """
        Finalize module session if needed.
        """

        # placeholder for future logic
        # example:
        # - mark session finished
        # - compute statistics
        # - save summary

        pass

    # -------------------------------------------------------
    # Lesson progression
    # -------------------------------------------------------
    def check_lesson_completion(self) -> bool:
        """
        Check if the entire lesson is finished.
        """

        lesson = self.module.training_lesson

        if not lesson:
            return False

        for module in lesson.modules:
            if not module.done:
                return False

        return True

    # -------------------------------------------------------
    # Response builder
    # -------------------------------------------------------
    def build_response(self) -> Dict[str, Any]:
        """
        Build UI response for module completion.
        """

        return {
            "type": "module_complete",
            "module_id": self.module.id,
            "module_type": self.module.module_type.value,
        }

    # -------------------------------------------------------
    # Debug helpers
    # -------------------------------------------------------
    def debug_info(self) -> Dict[str, Any]:
        """
        Debug information for monitoring.
        """

        return {
            "module_id": self.module.id,
            "done": self.module.done,
        }

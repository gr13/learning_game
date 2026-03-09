from typing import Dict, Any

from app.models.modules import ModulesModel
from app.models.sessions import SessionsModel


class ModuleAnalyzer:
    """
    Inspects module/session state and determines progress.
    """

    TOTAL_EXERCISES = 5

    def __init__(self, module: ModulesModel, session: SessionsModel):
        self.module = module
        self.session = session

    # -------------------------------------------------------
    # Main analysis entrypoint
    # -------------------------------------------------------
    def analyze(self) -> Dict[str, Any]:
        """
        Return current module state snapshot.
        """

        return {
            "module_id": self.module.id,
            "module_type": self.module.module_type.value,
            "exercise_index": self.get_current_exercise(),
            "is_complete": self.is_module_complete(),
        }

    # -------------------------------------------------------
    # Exercise position
    # -------------------------------------------------------
    def get_current_exercise(self) -> int:
        """
        Return current exercise number.
        """
        return self.session.get_current_exercise()

    def get_total_exercises(self) -> int:
        """
        Return total exercises in module.
        """

        return self.TOTAL_EXERCISES

    # -------------------------------------------------------
    # Module state
    # -------------------------------------------------------
    def is_module_complete(self) -> bool:
        """
        Check whether module should finish.
        """

        return self.get_current_exercise() > self.get_total_exercises()

    def should_continue(self) -> bool:
        """
        Determine if module should continue execution.
        """

        return not self.is_module_complete()

    def should_finalize(self) -> bool:
        """
        Determine if module should be finalized.
        """

        return self.is_module_complete()

    # -------------------------------------------------------
    # Debug / monitoring
    # -------------------------------------------------------
    def debug_info(self) -> Dict[str, Any]:
        """
        Provide debug information.
        """

        return {
            "module_id": self.module.id,
            "exercise": self.get_current_exercise(),
            "total_exercises": self.get_total_exercises(),
        }

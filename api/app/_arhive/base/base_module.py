from abc import ABC, abstractmethod
from typing import Any, Dict

from app.models.modules import ModulesModel
from app.models.sessions import SessionsModel


class BaseModule(ABC):
    """
    Base class for all learning modules.

    A module contains exercises and controls their execution.
    """

    def __init__(self, module: ModulesModel, session: SessionsModel):
        self.module = module
        self.session = session

    # -------------------------------------------------------
    # Main execution entrypoint
    # -------------------------------------------------------
    def run(self, user_input: str | None = None) -> Dict[str, Any]:
        """
        Execute module logic.

        Delegates to exercise engine.
        """

        if self.is_completed():
            return self.complete()

        return self.run_exercise(user_input)

    # -------------------------------------------------------
    # Exercise execution
    # -------------------------------------------------------
    @abstractmethod
    def run_exercise(self, user_input: str | None) -> Dict[str, Any]:
        """
        Execute current exercise.

        Implemented in module engines.
        """
        pass

    # -------------------------------------------------------
    # Module lifecycle
    # -------------------------------------------------------
    def initialize(self) -> None:
        """
        Module initialization logic.

        Called when module starts.
        """
        pass

    def complete(self) -> Dict[str, Any]:
        """
        Finalize module.
        """

        self.module.mark_done()

        return {
            "type": "module_complete",
            "module_id": self.module.id,
        }

    # -------------------------------------------------------
    # State helpers
    # -------------------------------------------------------
    def is_completed(self) -> bool:
        """
        Check if module is finished.
        """

        return self.module.done

    # -------------------------------------------------------
    # Progress helpers
    # -------------------------------------------------------
    def get_current_exercise(self) -> int:
        """
        Return current exercise index.
        """
        return self.session.exercise_index

        return 1

    def advance_exercise(self) -> None:
        """
        Move to next exercise.
        """
        self.session.advance_exercise()

    # -------------------------------------------------------
    # Plan loading
    # -------------------------------------------------------
    @abstractmethod
    def load_plan(self) -> Dict[str, Any]:
        """
        Load module plan configuration.
        """
        pass

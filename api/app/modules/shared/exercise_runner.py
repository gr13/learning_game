from typing import Dict, Any, Type

from app.modules.base.base_exercise import BaseExercise
from app.models.modules import ModulesModel
from app.models.sessions import SessionsModel


class ExerciseRunner:
    """
    Generic executor for exercises.
    """

    def __init__(self, module: ModulesModel, session: SessionsModel):
        self.module = module
        self.session = session

    # -------------------------------------------------------
    # Public entrypoint
    # -------------------------------------------------------
    def run(
        self,
        exercise_class: Type[BaseExercise],
        user_input: str | None = None
    ) -> Dict[str, Any]:
        """
        Execute exercise lifecycle.
        """

        exercise = self.create_exercise(exercise_class)

        return exercise.run(user_input)

    # -------------------------------------------------------
    # Exercise creation
    # -------------------------------------------------------
    def create_exercise(
        self,
        exercise_class: Type[BaseExercise]
    ) -> BaseExercise:
        """
        Instantiate exercise class.
        """

        return exercise_class(
            module=self.module,
            session=self.session
        )

    # -------------------------------------------------------
    # Session helpers
    # -------------------------------------------------------
    def get_current_exercise(self) -> int:
        """
        Return current exercise index.
        """
        return self.session.get_current_exercise()

    def advance_exercise(self) -> None:
        """
        Move to next exercise.
        """
        self.session.advance_exercise()

    # -------------------------------------------------------
    # Debug / monitoring
    # -------------------------------------------------------
    def debug_info(self) -> Dict[str, Any]:
        """
        Debug information for monitoring.
        """

        return {
            "module_id": self.module.id,
            "exercise_index": self.get_current_exercise(),
        }

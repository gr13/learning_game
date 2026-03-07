# modules/vocabulary/core/exercise_engine.py

from typing import Dict, Any, Type

from app.modules.base.base_exercise import BaseExercise
from app.modules.shared.exercise_runner import ExerciseRunner

# exercises
from .exercises.new_word_drill import NewWordDrill
from .exercises.repetition_drill import RepetitionDrill
from .exercises.context_usage_drill import ContextUsage
from .exercises.mixed_tense_drill import MixedTenseDrill
from .exercises.translation_drill import TranslationDrill


class CoreExerciseEngine:
    """
    Executes exercises for the Core Vocabulary module.

    Responsible for:
        - mapping exercise index → exercise class
        - delegating execution to ExerciseRunner
    """

    # -------------------------------------------------------
    # Exercise mapping (single source of truth)
    # -------------------------------------------------------

    EXERCISE_MAP: Dict[int, Type[BaseExercise]] = {
        1: NewWordDrill,
        2: RepetitionDrill,
        3: ContextUsage,
        4: MixedTenseDrill,
        5: TranslationDrill,
    }

    # -------------------------------------------------------
    # Initialization
    # -------------------------------------------------------
    def __init__(self, module, session):
        self.module = module
        self.session = session
        self.runner = ExerciseRunner(module, session)

    # -------------------------------------------------------
    # Main execution
    # -------------------------------------------------------
    def run(
            self, exercise_index: int, user_input: str | None
            ) -> Dict[str, Any]:
        """
        Execute the exercise corresponding to the index.
        """

        exercise_class = self.get_exercise_class(exercise_index)

        if not exercise_class:
            return self.build_error("Unknown exercise")

        return self.runner.run(exercise_class, user_input)

    # -------------------------------------------------------
    # Exercise selection
    # -------------------------------------------------------
    def get_exercise_class(self, index: int) -> Type[BaseExercise] | None:
        """
        Return exercise class for given index.
        """

        return self.EXERCISE_MAP.get(index)

    # -------------------------------------------------------
    # Helpers
    # -------------------------------------------------------
    def build_error(self, message: str) -> Dict[str, Any]:
        """
        Standard error response.
        """
        return {
            "type": "error",
            "message": message,
        }

    # -------------------------------------------------------
    # Debug / monitoring
    # -------------------------------------------------------

    def debug_info(self) -> Dict[str, Any]:
        """
        Debug information for monitoring.
        """
        return {
            "module_id": self.module.id,
            "exercise": getattr(self.session, "current_exercise", 1),
            "total_exercises": len(self.EXERCISE_MAP),
        }

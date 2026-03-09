from typing import Dict, Type, Any

from app.modules.base.base_exercise import BaseExercise

from app.modules.vocabulary.core.exercises.new_word_drill import NewWordDrill
from app.modules.vocabulary.core.exercises.repetition_drill import RepetitionDrill  # noqa: E501
from app.modules.vocabulary.core.exercises.context_usage_drill import ContextUsageDrill  # noqa: E501
from app.modules.vocabulary.core.exercises.mixed_tense_drill import MixedTenseDrill  # noqa: E501
from app.modules.vocabulary.core.exercises.translation_drill import TranslationDrill  # noqa: E501

from app.models.modules import ModulesModel
from app.models.sessions import SessionsModel


class CoreExerciseEngine:
    """
    Core vocabulary exercise dispatcher.

    Maps exercise index to exercise implementation.
    """
    EXERCISE_MAP: Dict[int, Type[BaseExercise]] = {
        1: NewWordDrill,
        2: RepetitionDrill,
        3: ContextUsageDrill,
        4: MixedTenseDrill,
        5: TranslationDrill,
    }

    # -------------------------------------------------------
    # Constructor
    # -------------------------------------------------------
    def __init__(self, module: ModulesModel, session: SessionsModel):
        self.module = module
        self.session = session

    # -------------------------------------------------------
    # Main execution
    # -------------------------------------------------------
    def run(
            self, exercise_index: int, user_input: str | None
            ) -> Dict[str, Any]:
        """
        Execute exercise based on index.
        """
        exercise_class = self.get_exercise_class(exercise_index)
        exercise = exercise_class(
            module=self.module,
            session=self.session
        )
        return exercise.run(user_input)

    # -------------------------------------------------------
    # Exercise resolution
    # -------------------------------------------------------
    def get_exercise_class(self, index: int) -> Type[BaseExercise]:
        """
        Resolve exercise class.
        """
        if index not in self.EXERCISE_MAP:
            raise ValueError(f"Unknown exercise index: {index}")
        return self.EXERCISE_MAP[index]

from typing import Dict, Any

from app.modules.templates.vocabulary_template import VocabularyTemplate
from app.modules.vocabulary.core.exercise_engine import CoreExerciseEngine


class CoreVocabularyModule(VocabularyTemplate):
    """
    Core Vocabulary learning module.

    Structure:
        5 exercises
        each exercise → 5 tasks
    """

    # -------------------------------------------------------
    # Main execution
    # -------------------------------------------------------
    def run_exercise(self, user_input: str | None) -> Dict[str, Any]:
        """
        Execute current vocabulary exercise.
        """

        exercise_index = self.get_current_exercise()

        engine = self.get_exercise_engine()

        return engine.run(exercise_index, user_input)

    # -------------------------------------------------------
    # Engine factory
    # -------------------------------------------------------
    def get_exercise_engine(self) -> CoreExerciseEngine:
        """
        Create exercise engine instance.
        """

        return CoreExerciseEngine(
            module=self.module,
            session=self.session
        )

    # -------------------------------------------------------
    # Context builder
    # -------------------------------------------------------
    def build_context(self) -> Dict[str, Any]:
        """
        Build context passed to exercises / prompts.
        """

        context = super().build_context()

        context.update({
            "module": "core_vocabulary",
            "exercise": self.get_current_exercise(),
        })

        return context

    # -------------------------------------------------------
    # Debug helpers
    # -------------------------------------------------------
    def debug_info(self) -> Dict[str, Any]:
        """
        Debug information for monitoring.
        """

        return {
            "module_id": self.module.id,
            "exercise": self.get_current_exercise(),
        }

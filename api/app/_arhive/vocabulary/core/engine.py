from typing import Dict, Any

from app.modules.templates.vocabulary_template import VocabularyTemplate
from app.modules.vocabulary.core.exercise_engine import CoreExerciseEngine

from app.models.modules import ModulesModel
from app.models.sessions import SessionsModel


class CoreVocabularyModule(VocabularyTemplate):
    """
    Core Vocabulary learning module.

    Flow:

        0 → word intro
        1 → new_word_drill
        2 → repetition_drill
        3 → context_usage
        4 → mixed_tense_drill
        5 → translation_drill
        6 → closing
    """
    # -------------------------------------------------------
    # Entry point used by ModuleEngine
    # -------------------------------------------------------
    def run(
            module: ModulesModel,
            session: SessionsModel,
            user_input: str | None = None
            ) -> Dict[str, Any]:
        """
        Entry point called from ModuleEngine.
        """
        module_runner = CoreVocabularyModule(module, session)
        return module_runner.execute(user_input)

    # -------------------------------------------------------
    # Main execution flow
    # -------------------------------------------------------
    def execute(self, user_input: str | None) -> Dict[str, Any]:
        """
        Control full module flow.
        """
        # Intro step
        if self.is_intro():
            result = self.run_intro()
            self.advance_exercise()
            return result

        # Closing step
        if self.is_closing():
            return self.run_closing()

        # Exercise step
        return self.run_exercise(user_input)

    # -------------------------------------------------------
    # Exercise execution
    # -------------------------------------------------------
    def run_exercise(self, user_input: str | None) -> Dict[str, Any]:
        """
        Execute vocabulary exercise.
        """

        exercise_index = self.get_current_exercise()
        engine = self.get_exercise_engine()
        return engine.run(exercise_index, user_input)

    # -------------------------------------------------------
    # Engine factory
    # -------------------------------------------------------
    def get_exercise_engine(self) -> CoreExerciseEngine:
        """
        Create exercise engine.
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
        Extend base context.
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
        Debug information.
        """
        return {
            "module_id": self.module.id,
            "exercise": self.get_current_exercise(),
        }


# -------------------------------------------------------
# Public engine function used by ModuleEngine
# -------------------------------------------------------
def run(
        module: ModulesModel,
        session: SessionsModel,
        user_input: str | None = None
        ) -> Dict[str, Any]:
    """
    Public module runner.

    This function is registered inside:

        MODULE_REGISTRY
    """
    return CoreVocabularyModule.run(module, session, user_input)

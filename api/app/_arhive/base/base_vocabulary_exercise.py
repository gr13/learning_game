from pathlib import Path
import json
from typing import Dict, Any

from app.modules.base.base_exercise import BaseExercise
from app.modules.shared.prompt_builder import PromptBuilder
from app.modules.shared.evaluation import EvaluationService


class BaseVocabularyExercise(BaseExercise):
    """
    Base class for vocabulary exercises (core + domain).
    """

    PLAN_FILE: str = ""
    EXERCISE_ID: int = 0

    # -------------------------------------------------------
    # Start exercise
    # -------------------------------------------------------
    def start(self) -> Dict[str, Any]:

        plan = self.load_plan()

        prompt = self.build_prompt(plan)

        return {
            "type": "exercise",
            "exercise": self.EXERCISE_ID,
            "instruction": plan.get("instruction"),
            "prompt": prompt,
        }

    # -------------------------------------------------------
    # Process user input
    # -------------------------------------------------------
    def process(self, user_input: str) -> Dict[str, Any]:

        plan = self.load_plan()

        evaluator = EvaluationService()

        return evaluator.evaluate_free_text(
            user_answer=user_input,
            expected_keywords=plan.get("keywords", []),
        )

    # -------------------------------------------------------
    # Prompt generation
    # -------------------------------------------------------
    def build_prompt(self, plan: Dict[str, Any]) -> str:

        builder = PromptBuilder()

        context = {
            "exercise": self.EXERCISE_ID
        }

        return builder.build(
            instruction=plan.get("instruction"),
            tasks=plan.get("tasks", []),
            context=context
        )

    # -------------------------------------------------------
    # Plan loading
    # -------------------------------------------------------
    def load_plan(self) -> Dict[str, Any]:

        path = Path(__file__).parent.parent / self.PLAN_FILE

        with open(path) as f:
            return json.load(f)

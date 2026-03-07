from typing import Dict, Any


class EvaluationService:
    """
    Generic evaluation logic for exercises.
    """

    # -------------------------------------------------------
    # Public evaluation entrypoints
    # -------------------------------------------------------
    def evaluate_translation(
        self,
        user_answer: str,
        correct_answer: str
    ) -> Dict[str, Any]:
        """
        Evaluate translation exercises.
        """

        normalized_user = self.normalize(user_answer)
        normalized_correct = self.normalize(correct_answer)

        is_correct = normalized_user == normalized_correct

        return self.build_result(
            is_correct,
            correct_answer,
            user_answer
        )

    def evaluate_multiple_choice(
        self,
        user_answer: str,
        correct_answer: str
    ) -> Dict[str, Any]:
        """
        Evaluate multiple choice tasks.
        """

        is_correct = user_answer == correct_answer

        return self.build_result(
            is_correct,
            correct_answer,
            user_answer
        )

    def evaluate_free_text(
        self,
        user_answer: str,
        expected_keywords: list[str]
    ) -> Dict[str, Any]:
        """
        Evaluate open text answers.
        """

        score = self.keyword_match_score(user_answer, expected_keywords)

        return {
            "correct": score > 0.7,
            "score": score,
            "user_answer": user_answer,
        }

    # -------------------------------------------------------
    # Scoring helpers
    # -------------------------------------------------------
    def keyword_match_score(
        self,
        text: str,
        keywords: list[str]
    ) -> float:
        """
        Simple keyword-based scoring.
        """

        if not keywords:
            return 0.0

        text = text.lower()

        matches = 0

        for keyword in keywords:
            if keyword.lower() in text:
                matches += 1

        return matches / len(keywords)

    # -------------------------------------------------------
    # Normalization
    # -------------------------------------------------------
    def normalize(self, text: str) -> str:
        """
        Normalize answers before comparison.
        """

        return text.strip().lower()

    # -------------------------------------------------------
    # Result builder
    # -------------------------------------------------------
    def build_result(
        self,
        is_correct: bool,
        correct_answer: str,
        user_answer: str
    ) -> Dict[str, Any]:
        """
        Standard evaluation response.
        """

        return {
            "correct": is_correct,
            "correct_answer": correct_answer,
            "user_answer": user_answer,
        }

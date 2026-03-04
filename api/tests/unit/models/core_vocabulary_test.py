import sys
from typing import Dict
# adding src to the system path
from pathlib import Path
sys.path.append(str(Path(sys.path[0]).parent))
sys.path.append(str(Path(sys.path[0]).parent.parent))
sys.path.append(str(Path(sys.path[0]).parent.parent.parent))
from app.models.core_vocabulary import CoreVocabularyModel  # noqa:E402
from tests.base_test import BaseTest  # noqa:E402


class CoreVocabularyTest(BaseTest):

    def core_vocabulary_json(self):
        """
        Creates core vocabulary model and checks the returned json
        """
        model = CoreVocabularyModel(word="test_word")
        model.save_to_db()

        saved = CoreVocabularyModel.find_by_id(model.id)
        self.assertIsNotNone(saved)

        expected = {
            "id": saved.id,
            "word": saved.word,
            "introduced": False,
            "dt_introduced": None,
            "learned": False,
            "dt_learned": None,
        }
        actual: Dict = saved.json()
        self.assertDictEqual(
            actual, expected,
            f"Core Vocabular JSON is incorrect expected: "
            f"{expected}, actual: {actual}")

    def test_state_transitions(self):
    
        model = CoreVocabularyModel(word="haus")
        model.save_to_db()

        model.mark_introduced()
        model.mark_learned()

        saved = CoreVocabularyModel.find_by_id(model.id)

        self.assertTrue(saved.introduced)
        self.assertTrue(saved.learned)
        self.assertIsNotNone(saved.dt_introduced)
        self.assertIsNotNone(saved.dt_learned)

        self.assertGreaterEqual(saved.dt_learned, saved.dt_introduced)

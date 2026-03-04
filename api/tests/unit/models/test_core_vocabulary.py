from app.models.core_vocabulary import CoreVocabularyModel


class TestCoreVocabulary:

    def test_core_vocabulary_json(self, db_session):
        """
        Creates core vocabulary model and checks the returned json
        """
        model = CoreVocabularyModel(word="test_word")
        model.save_to_db()

        saved = CoreVocabularyModel.find_by_id(model.id)
        assert saved is not None

        expected = {
            "id": saved.id,
            "word": saved.word,
            "introduced": False,
            "dt_introduced": None,
            "learned": False,
            "dt_learned": None,
        }
        assert saved.json() == expected

    def test_core_vocabulary_state_transitions(self, db_session):

        model = CoreVocabularyModel(word="haus")
        model.save_to_db()

        model.mark_introduced()
        model.mark_learned()

        saved = CoreVocabularyModel.find_by_id(model.id)

        assert saved.introduced is True
        assert saved.learned is True
        assert saved.dt_introduced is not None
        assert saved.dt_learned is not None
        assert saved.dt_learned >= saved.dt_introduced

    def test_core_vocabulary_find_new(self, db_session):

        task1 = CoreVocabularyModel(word="task1")
        task2 = CoreVocabularyModel(word="task2")

        task1.save_to_db()
        task2.save_to_db()

        task1.mark_introduced()

        new_task = CoreVocabularyModel.find_new()

        assert new_task.id == task2.id

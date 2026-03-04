from app.models.core_vocabulary import CoreVocabularyModel


class TestCoreVocabulary():

    def test_core_vocabulary_json(self, app):
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

    def test_state_transitions(self, app):

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

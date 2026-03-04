from app.models.domain_vocabulary import DomainVocabularyModel


class TestDomainVocabulary:

    def test_domain_vocabulary_json(self, db_session):
        """
        Creates domain vocabulary model and checks the returned json
        """
        model = DomainVocabularyModel(word="test_word", domain="test_domain")
        model.save_to_db()

        saved = DomainVocabularyModel.find_by_id(model.id)
        assert saved is not None

        expected = {
            "id": saved.id,
            "word": saved.word,
            "domain": saved.domain,
            "introduced": False,
            "dt_introduced": None,
            "learned": False,
            "dt_learned": None,
        }
        assert saved.json() == expected

    def test_domain_vocabulary_state_transitions(self, db_session):

        model = DomainVocabularyModel(word="haus", domain="test_domain")
        model.save_to_db()

        model.mark_introduced()
        model.mark_learned()

        saved = DomainVocabularyModel.find_by_id(model.id)

        assert saved.introduced is True
        assert saved.learned is True
        assert saved.dt_introduced is not None
        assert saved.dt_learned is not None
        assert saved.dt_learned >= saved.dt_introduced

    def test_domain_vocabulary_find_new(self, db_session):

        task1 = DomainVocabularyModel(word="task1", domain="test_domain")
        task2 = DomainVocabularyModel(word="task2", domain="test_domain")

        task1.save_to_db()
        task2.save_to_db()

        task1.mark_introduced()

        new_task = DomainVocabularyModel.find_new()

        assert new_task.id == task2.id

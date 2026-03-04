from app.models.writing_exam import WritingExamModel
from app.enums import LevelEnum


class TestWritingExam:

    def test_writing_exam_json(self, db_session):
        """
        Creates writing exam model and checks the returned json
        """
        model = WritingExamModel(
            main_task="task_level test", task_level=LevelEnum.A2)
        model.save_to_db()

        saved = WritingExamModel.find_by_id(model.id)
        assert saved is not None

        expected = {
            "id": saved.id,
            "task_level": "A2",
            "main_task": "task_level test",
            "done": False,
            "dt_done": None,
        }
        assert saved.json() == expected

    def test_writing_exam_state_transitions(self, db_session):

        model = WritingExamModel(
            main_task="task_level test", task_level=LevelEnum.A2)
        model.save_to_db()

        model.mark_done()

        saved = WritingExamModel.find_by_id(model.id)

        assert saved.done is True
        assert saved.dt_done is not None

from app.models.reading_exam import ReadingExamModel
from app.enums import LevelEnum


class TestReadingExam:

    def test_reading_exam_json(self, db_session):
        """
        Creates reading exam model and checks the returned json
        """
        model = ReadingExamModel(
            main_task="task_level test", task_level=LevelEnum.A2)
        model.save_to_db()

        saved = ReadingExamModel.find_by_id(model.id)
        assert saved is not None

        expected = {
            "id": saved.id,
            "task_level": "A2",
            "main_task": saved.main_task,
            "done": False,
            "dt_done": None,
        }
        assert saved.json() == expected

    def test_reading_exam_state_transitions(self, db_session):

        model = ReadingExamModel(
            main_task="task_level test", task_level=LevelEnum.A2)
        model.save_to_db()

        model.mark_done()

        saved = ReadingExamModel.find_by_id(model.id)

        assert saved.done is True
        assert saved.dt_done is not None

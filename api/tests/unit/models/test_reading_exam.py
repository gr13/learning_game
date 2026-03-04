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

    def test_reading_exam_find_new(self, db_session):

        task1 = ReadingExamModel(main_task="task1", task_level=LevelEnum.A2)
        task2 = ReadingExamModel(main_task="task2", task_level=LevelEnum.A2)

        task1.save_to_db()
        task2.save_to_db()

        task1.mark_done()

        new_task = ReadingExamModel.find_new()

        assert new_task.id == task2.id

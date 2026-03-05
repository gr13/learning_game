from app.models.training_lesson import TrainingLessonModel
from app.enums import LevelEnum


class TestTrainingLesson:

    def test_training_lesson_json(self, db_session):
        """
        Creates speaking exam model and checks the returned json
        """
        model = TrainingLessonModel(user_level=LevelEnum.A2)
        model.save_to_db()

        saved = TrainingLessonModel.find_by_id(model.id)
        assert saved is not None

        expected = {
            "id": model.id,
            "user_level": "A2",
            "modules": [],
            "ts": model.ts.strftime("%d.%m.%Y %H:%M") if model.ts else None,
            "done": False,
        }

        assert saved.json() == expected

    def test_training_lesson_state_transitions(self, db_session):

        model = TrainingLessonModel(user_level=LevelEnum.A2)
        model.save_to_db()

        model.mark_done()

        saved = TrainingLessonModel.find_by_id(model.id)

        assert saved.done is True

    def test_training_lesson_find_new(self, db_session):

        task1 = TrainingLessonModel(user_level=LevelEnum.A2)
        task2 = TrainingLessonModel(user_level=LevelEnum.A2)

        task1.save_to_db()
        task2.save_to_db()

        task1.mark_done()

        new_task = TrainingLessonModel.find_last_active()

        assert new_task.id == task2.id

    def test_training_lesson_find_by_id_not_found(self, db_session):

        lesson = TrainingLessonModel.find_by_id(9999)

        assert lesson is None

    def test_training_lesson_find_last_active_none(self, db_session):

        lesson = TrainingLessonModel(user_level=LevelEnum.A2)
        lesson.save_to_db()
        lesson.mark_done()

        result = TrainingLessonModel.find_last_active()

        assert result is None

    def test_training_lesson_mark_all_as_done(self, db_session):

        l1 = TrainingLessonModel(user_level=LevelEnum.A2)
        l2 = TrainingLessonModel(user_level=LevelEnum.A2)

        l1.save_to_db()
        l2.save_to_db()

        TrainingLessonModel.mark_all_as_done()

        lessons = TrainingLessonModel.find_all()

        for lesson in lessons:
            assert lesson.done is True

    def test_training_lesson_find_all_not_done(self, db_session):

        l1 = TrainingLessonModel(user_level=LevelEnum.A2)
        l2 = TrainingLessonModel(user_level=LevelEnum.A2)

        l1.save_to_db()
        l2.save_to_db()

        l1.mark_done()

        not_done = TrainingLessonModel.find_all_not_done()

        assert len(not_done) == 1
        assert not_done[0].id == l2.id

    def test_training_lesson_timestamp_created(self, db_session):

        lesson = TrainingLessonModel(user_level=LevelEnum.A2)
        lesson.save_to_db()

        saved = TrainingLessonModel.find_by_id(lesson.id)

        assert saved.ts is not None

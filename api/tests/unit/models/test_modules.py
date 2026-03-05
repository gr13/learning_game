import pytest
from app.models.modules import ModulesModel
from app.models.training_lesson import TrainingLessonModel
from app.enums import ModuleTypeEnum, LevelEnum


class TestModules:

    def test_modules_json(self, db_session):
        """
        Creates speaking exam model and checks the returned json
        """
        lesson = TrainingLessonModel(user_level=LevelEnum.A2)
        lesson.save_to_db()

        module = ModulesModel(
            training_lesson_id=lesson.id,
            module_type=ModuleTypeEnum.CORE
        )
        module.save_to_db()

        saved = ModulesModel.find_by_id(module.id)
        assert saved is not None

        expected = {
            "id": saved.id,
            "training_lesson_id": lesson.id,
            "training_lesson": lesson.json_safe(),
            "module_type": "CORE",
            "done": saved.done,
        }

        assert saved.json() == expected

    def test_modules_find_by_lesson(self, db_session):

        lesson = TrainingLessonModel(user_level=LevelEnum.A2)
        lesson.save_to_db()

        m1 = ModulesModel(
            training_lesson_id=lesson.id,
            module_type=ModuleTypeEnum.CORE
        )

        m2 = ModulesModel(
            training_lesson_id=lesson.id,
            module_type=ModuleTypeEnum.READING
        )

        m1.save_to_db()
        m2.save_to_db()

        modules = ModulesModel.find_by_lesson(lesson.id)

        assert len(modules) == 2

    def test_modules_find_by_id_not_found(self, db_session):

        module = ModulesModel.find_by_id(9999)

        assert module is None

    def test_modules_relationship(self, db_session):

        lesson = TrainingLessonModel(user_level=LevelEnum.A2)
        lesson.save_to_db()

        module = ModulesModel(
            training_lesson_id=lesson.id,
            module_type=ModuleTypeEnum.CORE
        )
        module.save_to_db()

        saved = ModulesModel.find_by_id(module.id)

        assert saved.training_lesson.id == lesson.id

    def test_training_lesson_modules_relationship(self, db_session):

        lesson = TrainingLessonModel(user_level=LevelEnum.A2)
        lesson.save_to_db()

        m1 = ModulesModel(
            training_lesson_id=lesson.id,
            module_type=ModuleTypeEnum.CORE
        )

        m2 = ModulesModel(
            training_lesson_id=lesson.id,
            module_type=ModuleTypeEnum.READING
        )

        m1.save_to_db()
        m2.save_to_db()

        saved = TrainingLessonModel.find_by_id(lesson.id)

        modules = saved.modules

        assert len(modules) == 2

    def test_modules_enum_value(self, db_session):

        lesson = TrainingLessonModel(user_level=LevelEnum.A2)
        lesson.save_to_db()

        module = ModulesModel(
            training_lesson_id=lesson.id,
            module_type=ModuleTypeEnum.READING
        )

        module.save_to_db()

        saved = ModulesModel.find_by_id(module.id)

        assert saved.module_type == ModuleTypeEnum.READING

    def test_find_by_lesson_isolated(self, db_session):

        lesson1 = TrainingLessonModel(user_level=LevelEnum.A2)
        lesson2 = TrainingLessonModel(user_level=LevelEnum.A2)

        lesson1.save_to_db()
        lesson2.save_to_db()

        m1 = ModulesModel(
            training_lesson_id=lesson1.id,
            module_type=ModuleTypeEnum.CORE
        )

        m2 = ModulesModel(
            training_lesson_id=lesson2.id,
            module_type=ModuleTypeEnum.READING
        )

        m1.save_to_db()
        m2.save_to_db()

        modules = ModulesModel.find_by_lesson(lesson1.id)

        assert len(modules) == 1
        assert modules[0].training_lesson_id == lesson1.id

    def test_modules_json_safe(self, db_session):

        lesson = TrainingLessonModel(user_level=LevelEnum.A2)
        lesson.save_to_db()

        module = ModulesModel(
            training_lesson_id=lesson.id,
            module_type=ModuleTypeEnum.CORE
        )

        module.save_to_db()

        saved = ModulesModel.find_by_id(module.id)

        expected = {
            "id": saved.id,
            "training_lesson_id": lesson.id,
            "module_type": "CORE",
            "done": saved.done,
        }

        assert saved.json_safe() == expected

    def test_modules_invalid_lesson(self, db_session):

        module = ModulesModel(
            training_lesson_id=9999,
            module_type=ModuleTypeEnum.CORE
        )

        with pytest.raises(Exception):
            module.save_to_db()

    def test_modules_mark_done(self, db_session):

        lesson = TrainingLessonModel(user_level=LevelEnum.A2)
        lesson.save_to_db()

        module = ModulesModel(
            training_lesson_id=lesson.id,
            module_type=ModuleTypeEnum.CORE
        )
        module.save_to_db()

        module.mark_done()

        saved = ModulesModel.find_by_id(module.id)

        assert saved.done is True

    def test_modules_find_not_done(self, db_session):

        lesson = TrainingLessonModel(user_level=LevelEnum.A2)
        lesson.save_to_db()

        m1 = ModulesModel(
            training_lesson_id=lesson.id,
            module_type=ModuleTypeEnum.CORE
        )

        m2 = ModulesModel(
            training_lesson_id=lesson.id,
            module_type=ModuleTypeEnum.READING
        )

        m1.save_to_db()
        m2.save_to_db()

        m1.mark_done()

        not_done = ModulesModel.find_not_done(lesson.id)

        assert len(not_done) == 1
        assert not_done[0].id == m2.id

    def test_modules_find_all(self, db_session):

        lesson = TrainingLessonModel(user_level=LevelEnum.A2)
        lesson.save_to_db()

        m1 = ModulesModel(
            training_lesson_id=lesson.id,
            module_type=ModuleTypeEnum.CORE
        )

        m2 = ModulesModel(
            training_lesson_id=lesson.id,
            module_type=ModuleTypeEnum.READING
        )

        m1.save_to_db()
        m2.save_to_db()

        modules = ModulesModel.find_all()

        assert len(modules) >= 2

    def test_modules_default_values(self, db_session):

        lesson = TrainingLessonModel(user_level=LevelEnum.A2)
        lesson.save_to_db()

        module = ModulesModel(training_lesson_id=lesson.id)

        module.save_to_db()

        saved = ModulesModel.find_by_id(module.id)

        assert saved.module_type == ModuleTypeEnum.CORE
        assert saved.done is False

    def test_modules_json_after_done(self, db_session):

        lesson = TrainingLessonModel(user_level=LevelEnum.A2)
        lesson.save_to_db()

        module = ModulesModel(
            training_lesson_id=lesson.id,
            module_type=ModuleTypeEnum.CORE
        )

        module.save_to_db()
        module.mark_done()

        saved = ModulesModel.find_by_id(module.id)

        result = saved.json()

        assert result["done"] is True

    def test_find_by_lesson_empty(self, db_session):

        lesson = TrainingLessonModel(user_level=LevelEnum.A2)
        lesson.save_to_db()

        modules = ModulesModel.find_by_lesson(lesson.id)

        assert modules == []

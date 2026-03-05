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

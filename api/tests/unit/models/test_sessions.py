import uuid
from app.models.sessions import SessionsModel
from app.models.modules import ModulesModel
from app.models.training_lesson import TrainingLessonModel
from app.enums import ModuleTypeEnum, LevelEnum


class TestSessions:

    def create_module(self):
        lesson = TrainingLessonModel(user_level=LevelEnum.A2)
        lesson.save_to_db()

        module = ModulesModel(
            training_lesson_id=lesson.id,
            module_type=ModuleTypeEnum.CORE
        )
        module.save_to_db()

        return module

    def test_session_json(self, db_session):

        module = self.create_module()

        session = SessionsModel(
            module_id=module.id,
            session_id=str(uuid.uuid4())
        )
        session.save_to_db()

        saved = SessionsModel.find_by_id(session.id)

        expected = {
            "id": session.id,
            "ts": session.ts.strftime("%d.%m.%Y %H:%M"),
            "module_id": module.id,
            "module": module.json_safe(),
            "session_id": session.session_id,
        }

        assert saved.json() == expected

    def test_session_json_safe(self, db_session):

        module = self.create_module()

        session = SessionsModel(
            module_id=module.id,
            session_id=str(uuid.uuid4())
        )
        session.save_to_db()

        saved = SessionsModel.find_by_id(session.id)

        expected = {
            "id": session.id,
            "ts": session.ts.strftime("%d.%m.%Y %H:%M"),
            "module_id": module.id,
            "session_id": session.session_id,
        }

        assert saved.json_safe() == expected

    def test_session_find_by_id_not_found(self, db_session):

        result = SessionsModel.find_by_id(9999)

        assert result is None

    def test_session_find_by_module_id(self, db_session):

        module = self.create_module()

        s1 = SessionsModel(
            module_id=module.id,
            session_id=str(uuid.uuid4())
        )

        s2 = SessionsModel(
            module_id=module.id,
            session_id=str(uuid.uuid4())
        )

        s1.save_to_db()
        s2.save_to_db()

        sessions = SessionsModel.find_by_module_id(module.id)

        assert len(sessions) == 2

    def test_session_find_by_session_id(self, db_session):

        module = self.create_module()

        sid = str(uuid.uuid4())

        session = SessionsModel(
            module_id=module.id,
            session_id=sid
        )

        session.save_to_db()

        saved = SessionsModel.find_by_session_id(sid)

        assert saved.id == session.id

    def test_session_timestamp_created(self, db_session):

        module = self.create_module()

        session = SessionsModel(
            module_id=module.id,
            session_id=str(uuid.uuid4())
        )

        session.save_to_db()

        saved = SessionsModel.find_by_id(session.id)

        assert saved.ts is not None

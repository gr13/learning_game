from app.models.session_messages import SessionMessagesModel
from app.models.sessions import SessionsModel
from app.models.modules import ModulesModel
from app.models.training_lesson import TrainingLessonModel
from app.enums import ModuleTypeEnum, LevelEnum


class TestSessionMessages:

    def create_session(self):

        lesson = TrainingLessonModel(user_level=LevelEnum.A2)
        lesson.save_to_db()

        module = ModulesModel(
            training_lesson_id=lesson.id,
            module_type=ModuleTypeEnum.CORE
        )
        module.save_to_db()

        session = SessionsModel(
            module_id=module.id,
        )
        session.save_to_db()

        return session

    def test_session_message_json(self, db_session):

        session = self.create_session()

        message = SessionMessagesModel(
            session_id=session.id,
            role="user",
            content="Hallo",
            current_exercise=1
        )

        message.save_to_db()

        saved = SessionMessagesModel.find_by_session(session.id)[0]

        expected = {
            "id": message.id,
            "ts": message.ts.strftime("%d.%m.%Y %H:%M"),
            "session_id": session.id,
            "role": "user",
            "content": "Hallo",
            "current_exercise": 1,
        }

        assert saved.json() == expected

    def test_session_message_json_safe(self, db_session):

        session = self.create_session()

        message = SessionMessagesModel(
            session_id=session.id,
            role="assistant",
            content="Hallo zurück"
        )

        message.save_to_db()

        saved = SessionMessagesModel.find_by_session(session.id)[0]

        expected = {
            "id": message.id,
            "role": "assistant",
            "content": "Hallo zurück",
        }

        assert saved.json_safe() == expected

    def test_session_message_find_by_session(self, db_session):

        session = self.create_session()

        m1 = SessionMessagesModel(
            session_id=session.id,
            role="user",
            content="Hallo"
        )

        m2 = SessionMessagesModel(
            session_id=session.id,
            role="assistant",
            content="Hi"
        )

        m1.save_to_db()
        m2.save_to_db()

        messages = SessionMessagesModel.find_by_session(session.id)

        assert len(messages) == 2

    def test_session_message_find_last_message(self, db_session):

        session = self.create_session()

        m1 = SessionMessagesModel(
            session_id=session.id,
            role="user",
            content="Hallo"
        )

        m2 = SessionMessagesModel(
            session_id=session.id,
            role="assistant",
            content="Hi"
        )

        m1.save_to_db()
        m2.save_to_db()

        last = SessionMessagesModel.find_by_session(session.id)[-1]

        assert last.content == "Hi"

    def test_session_message_timestamp_created(self, db_session):

        session = self.create_session()

        message = SessionMessagesModel(
            session_id=session.id,
            role="user",
            content="Hallo"
        )

        message.save_to_db()

        saved = SessionMessagesModel.find_by_session(session.id)[0]

        assert saved.ts is not None

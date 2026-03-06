from app.db import db
from sqlalchemy import Enum


class SessionMessagesModel(db.Model):
    __tablename__ = "session_messages"

    id = db.Column(db.Integer, primary_key=True)

    ts = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now()
    )

    session_id = db.Column(
        db.Integer,
        db.ForeignKey("sessions.id"),
        nullable=False,
        index=True
    )

    session = db.relationship(
        "SessionsModel",
        back_populates="messages",
        lazy="selectin"
    )

    current_exercise = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    role = db.Column(
        Enum(
            "assistant",
            "user",
            "system",
            "error",
            "correction",
            "summary",
            name="message_role_enum"
        ),
        nullable=False,
        default="system"
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    def json(self):
        return {
            "id": self.id,
            "ts": self.ts.strftime("%d.%m.%Y %H:%M"),
            "session_id": self.session_id,
            "role": self.role,
            "content": self.content,
            "current_exercise": self.current_exercise,
        }

    def json_safe(self):
        return {
            "id": self.id,
            "role": self.role,
            "content": self.content,
        }

    @classmethod
    def find_by_session(cls, session_id: int):
        return (
            cls.query
            .filter_by(session_id=session_id)
            .order_by(cls.id)
            .all()
        )

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

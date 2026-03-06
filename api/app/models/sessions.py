# import logging
from app.db import db


class SessionsModel(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True)
    ts = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now()
    )
    session_id = db.Column(
        db.String(36),
        nullable=False,
        unique=True,
        index=True
    )

    module_id = db.Column(
        db.Integer,
        db.ForeignKey("modules.id"),
        nullable=False
    )

    module = db.relationship(
        "ModulesModel",
        back_populates="sessions",
        lazy="selectin"
    )

    messages = db.relationship(
        "SessionMessagesModel",
        back_populates="session",
        lazy="selectin",
        order_by="SessionMessagesModel.id",
        cascade="all, delete-orphan"
    )

    def json(self):
        """
        Return json representation of the class
        """
        return {
            "id": self.id,
            "ts": self.ts.strftime("%d.%m.%Y %H:%M"),
            "module_id": self.module_id,
            "module": self.module.json_safe() if self.module else None,
            "session_id": self.session_id,
        }

    def json_safe(self):
        return {
            "id": self.id,
            "ts": self.ts.strftime("%d.%m.%Y %H:%M"),
            "module_id": self.module_id,
            "session_id": self.session_id,
        }

    # ----------------------------
    # Queries
    # ----------------------------
    @classmethod
    def find_by_id(cls, _id: int):
        return db.session.get(cls, _id)

    @classmethod
    def find_by_module_id(cls, module_id: int):
        return (
            cls.query
            .filter_by(module_id=module_id)
            .order_by(cls.id)
            .all()
        )

    @classmethod
    def find_by_session_id(cls, session_id: str):
        return cls.query.filter_by(session_id=session_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    # ----------------------------
    # State transitions
    # ----------------------------

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

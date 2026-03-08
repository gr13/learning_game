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
        }

    def json_safe(self):
        return {
            "id": self.id,
            "ts": self.ts.strftime("%d.%m.%Y %H:%M"),
            "module_id": self.module_id,
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
    def find_all(cls):
        return cls.query.all()

    def get_exercise_index(self) -> int:
        """
        Return current exercise index.
        """
        return self.exercise_index or 0

    # ----------------------------
    # State transitions
    # ----------------------------
    def advance_exercise(self):
        """
        Move session to the next exercise step.
        """

        self.exercise_index = (self.exercise_index or 0) + 1
        self.save_to_db()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

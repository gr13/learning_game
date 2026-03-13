from __future__ import annotations
from app.db import db


class ExercisesModel(db.Model):
    __tablename__ = "exercises"

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

    session_id = db.Column(
        db.Integer,
        db.ForeignKey("sessions.id"),
        nullable=False,
        index=True,
    )

    session = db.relationship(
        "SessionsModel",
        back_populates="exercises",
        lazy="selectin",
    )

    module = db.relationship(
        "ModulesModel",
        back_populates="exercises",
        lazy="selectin",
    )

    exercise_index = db.Column(db.Integer, nullable=False, default=0)

    def json(self):
        """
        Return json representation of the class
        """
        return {
            "id": self.id,
            "ts": self.ts.strftime("%d.%m.%Y %H:%M"),
            "module_id": self.module_id,
            "session_id": self.session_id,
            "module": self.module.json_safe() if self.module else None,
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
    def find_by_session_id(cls, session_id: int) -> "ExercisesModel | None":
        return (
            cls.query
            .filter_by(session_id=session_id)
            .order_by(cls.id)
            .first()
        )

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def get_current_exercise(self) -> int:
        """
        Return current exercise index.
        """
        return self.exercise_index

    # ----------------------------
    # State transitions
    # ----------------------------

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

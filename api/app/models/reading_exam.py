# import logging
from datetime import datetime, UTC
from sqlalchemy import Enum
from app.db import db
from app.enums import LevelEnum


class ReadingExamModel(db.Model):
    __tablename__ = "reading_exam"

    id = db.Column(db.Integer, primary_key=True)
    task_level = db.Column(
        Enum(LevelEnum),
        nullable=False,
        default=LevelEnum.A2
    )
    main_task = db.Column(db.Text, nullable=False)
    done = db.Column(db.Boolean, nullable=False, default=False)
    dt_done = db.Column(db.DateTime, nullable=True)

    def json(self):
        """
        Return json representation of the class
        """
        return {
            "id": self.id,
            "task_level": self.task_level.value,
            "main_task": self.main_task,
            "done": self.done,
            "dt_done": self.dt_done.isoformat() if self.dt_done else None,  # noqa: E501
        }

    # ----------------------------
    # Queries
    # ----------------------------
    @classmethod
    def find_by_id(cls, _id: int):
        return db.session.get(cls, _id)

    @classmethod
    def find_new(cls):
        return cls.query.filter_by(done=False).order_by(cls.id).first()

    @classmethod
    def find_done(cls):
        return cls.query.filter_by(done=True).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    # ----------------------------
    # State transitions
    # ----------------------------

    def mark_done(self):
        self.done = True
        self.dt_done = datetime.now(UTC)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

# import logging
from app.db import db
from sqlalchemy import Enum
from app.enums import ModuleTypeEnum


class ModulesModel(db.Model):
    __tablename__ = "modules"

    id = db.Column(db.Integer, primary_key=True)
    training_lesson_id = db.Column(
        db.Integer,
        db.ForeignKey("training_lesson.id"),
        nullable=False
    )

    training_lesson = db.relationship(
        "TrainingLessonModel",
        back_populates="modules",
    )

    module_type = db.Column(
        Enum(ModuleTypeEnum, name="module_type_enum"),
        nullable=False,
        default=ModuleTypeEnum.CORE
    )

    def json(self):
        """
        Return json representation of the class
        """
        return {
            "id": self.id,
            "training_lesson_id": self.training_lesson_id,
            "training_lesson": self.training_lesson.json_safe(),
            "module_type": self.module_type.value,
        }

    def json_safe(self):
        return {
            "id": self.id,
            "training_lesson_id": self.training_lesson_id,
            "module_type": self.module_type.value,
        }

    # ----------------------------
    # Queries
    # ----------------------------
    @classmethod
    def find_by_id(cls, _id: int):
        return db.session.get(cls, _id)

    @classmethod
    def find_by_lesson(cls, lesson_id: int):
        return cls.query.filter_by(training_lesson_id=lesson_id).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    # ----------------------------
    # State transitions
    # ----------------------------

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

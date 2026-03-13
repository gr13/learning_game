# import logging
from app.db import db
from sqlalchemy import Enum
from app.enums import ModuleTypeEnum
from app.models.sessions import SessionsModel


class ModulesModel(db.Model):
    __tablename__ = "modules"

    id = db.Column(db.Integer, primary_key=True)
    training_lesson_id = db.Column(
        db.Integer,
        db.ForeignKey("training_lesson.id"),
        nullable=True,
        index=True
    )

    training_lesson = db.relationship(
        "TrainingLessonModel",
        back_populates="modules",
        lazy="selectin",
    )

    sessions = db.relationship(
        "SessionsModel",
        back_populates="module",
        lazy="selectin",
        order_by=lambda: SessionsModel.id,
        cascade="all, delete-orphan"
    )

    module_type = db.Column(
        Enum(ModuleTypeEnum, name="module_type_enum"),
        nullable=False,
        default=ModuleTypeEnum.CORE
    )

    done = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        index=True
    )

    exercises = db.relationship(
        "ExercisesModel",
        back_populates="module",
        lazy="selectin",
        order_by="ExercisesModel.id",
        cascade="all, delete-orphan",
    )

    def json(self):
        """
        Return json representation of the class
        """
        return {
            "id": self.id,
            "training_lesson_id": self.training_lesson_id,
            "training_lesson": self.training_lesson.json_safe() if self.training_lesson else None,  # noqa: E501
            "module_type": self.module_type.value,
            "done": self.done,
        }

    def json_safe(self):
        return {
            "id": self.id,
            "training_lesson_id": self.training_lesson_id,
            "module_type": self.module_type.value,
            "done": self.done,
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

    @classmethod
    def find_not_done(cls, lesson_id: int):
        return cls.query.filter_by(
            training_lesson_id=lesson_id,
            done=False
        ).all()

    @classmethod
    def get_module_type(cls) -> str:
        return cls.module_type

    # ----------------------------
    # State transitions
    # ----------------------------
    def mark_done(self):
        self.done = True
        self.save_to_db()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # ----------------------------
    # static
    # ----------------------------
    @staticmethod
    def module_type_from_module_id(
        module_type_id: int
    ) -> ModuleTypeEnum | None:
        mapping = {
            1: ModuleTypeEnum.CORE,
            2: ModuleTypeEnum.DOMAIN,
            3: ModuleTypeEnum.READING,
            4: ModuleTypeEnum.WRITING,
            5: ModuleTypeEnum.SPEAKING,
        }
        return mapping.get(module_type_id)

    @staticmethod
    def module_id_from_module_type(
        module_type: ModuleTypeEnum
    ) -> int | None:
        mapping = {
            ModuleTypeEnum.CORE: 1,
            ModuleTypeEnum.DOMAIN: 2,
            ModuleTypeEnum.READING: 3,
            ModuleTypeEnum.WRITING: 4,
            ModuleTypeEnum.SPEAKING: 5,
        }
        return mapping.get(module_type)

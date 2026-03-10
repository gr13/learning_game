from app.db import db
from sqlalchemy import Enum
from app.enums import LevelEnum


class TrainingLessonModel(db.Model):
    __tablename__ = "training_lesson"

    id = db.Column(db.Integer, primary_key=True)
    user_level = db.Column(
        Enum(LevelEnum, name="user_level_enum"),
        nullable=False,
        default=LevelEnum.A2
    )
    ts = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    done = db.Column(db.Boolean, nullable=False, default=False)

    # lazy="dynamic" does not create the list of items
    # unless it is necessary
    modules = db.relationship(
        "ModulesModel",
        back_populates="training_lesson",
        lazy="selectin"
    )

    def json(self):
        """
        Return json representation of the class
        """
        return {
            "id": self.id,
            "user_level": self.user_level.value,
            "modules": [module.json() for module in self.modules] if self.modules else [],  # noqa:E501
            "ts": self.ts.strftime("%d.%m.%Y %H:%M") if self.ts else None,
            "done": self.done,
        }

    def json_safe(self):
        """
        Return json safe representation of the class
        """
        return {
            "id": self.id,
            "user_level": self.user_level.value,
            "ts": self.ts.strftime("%d.%m.%Y %H:%M") if self.ts else None,
            "done": self.done,
        }

    # ----------------------------
    # Queries
    # ----------------------------
    @classmethod
    def find_by_id(cls, _id: int):
        return db.session.get(cls, _id)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_last_active(cls):
        return cls.query.filter_by(done=False).order_by(cls.id.desc()).first()

    @classmethod
    def find_all_not_done(cls):
        return cls.query.filter_by(done=False).all()

    # ----------------------------
    # State transitions
    # ----------------------------
    @classmethod
    def mark_all_as_done(cls):
        cls.query.filter_by(done=False).update(
            {"done": True},
            synchronize_session=False
        )
        db.session.commit()

    def mark_done(self):
        self.done = True
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

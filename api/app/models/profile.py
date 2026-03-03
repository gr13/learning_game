# import logging
from app.db import db
import enum
from sqlalchemy import Enum


class LevelEnum(enum.Enum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"

# initialization: profile = Profile(user_level=LevelEnum.B1)


class ProfileModel(db.Model):
    __tablename__ = "profile"

    id = db.Column(db.Integer, primary_key=True)
    user_level = db.Column(
        Enum(LevelEnum),
        nullable=False,
        default=LevelEnum.A2
    )
    preferences = db.Column(db.String(255), nullable=False, default="")

    def json(self):
        """
        Return json representation of the class
        """
        return {
            "id": self.id,
            "user_level": self.user_level.value,
            "preferences": self.preferences,
        }

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.get(_id)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

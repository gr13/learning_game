# import logging
from app.db import db
from sqlalchemy import Enum
from app.enums import LevelEnum

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

    # ----------------------------
    # Queries
    # ----------------------------
    @classmethod
    def find_by_id(cls, _id: int = 1):
        return db.session.get(cls, _id)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def get_user_level(self):
        return self.user_level.value

    # ----------------------------
    # State transitions
    # ----------------------------
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

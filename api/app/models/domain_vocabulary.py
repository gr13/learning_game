# import logging
from datetime import datetime, UTC
from app.db import db


class DomainVocabularyModel(db.Model):
    __tablename__ = "domain_vocabulary"

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(255), nullable=False, unique=True)
    domain = db.Column(db.String(100), nullable=False)
    introduced = db.Column(db.Boolean, nullable=False, default=False)
    dt_introduced = db.Column(db.DateTime, nullable=True)
    learned = db.Column(db.Boolean, nullable=False, default=False)
    dt_learned = db.Column(db.DateTime, nullable=True)

    def json(self):
        """
        Return json representation of the class
        """
        return {
            "id": self.id,
            "word": self.word,
            "domain": self.domain,
            "introduced": self.introduced,
            "dt_introduced": self.dt_introduced.isoformat() if self.dt_introduced else None,  # noqa: E501
            "learned": self.learned,
            "dt_learned": self.dt_learned.isoformat() if self.dt_learned else None,  # noqa: E501
        }

    # ----------------------------
    # Queries
    # ----------------------------
    @classmethod
    def find_by_id(cls, _id: int):
        return db.session.get(cls, _id)

    @classmethod
    def find_new(cls):
        return cls.query.filter_by(introduced=False).first()

    @classmethod
    def find_introduced(cls):
        return cls.query.filter_by(introduced=True).order_by(cls.id).all()

    @classmethod
    def find_learned(cls):
        return cls.query.filter_by(learned=True).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    # ----------------------------
    # State transitions
    # ----------------------------

    def mark_introduced(self):
        self.introduced = True
        self.dt_introduced = datetime.now(UTC)
        db.session.commit()

    def mark_learned(self):
        self.learned = True
        self.dt_learned = datetime.now(UTC)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

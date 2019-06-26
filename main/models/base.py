import datetime

from sqlalchemy import Column, Integer, DateTime

from main.database import db


class BaseModel(db.Model):
    """Provides common common interface for model"""

    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    updated = Column(DateTime,
                     default=datetime.datetime.utcnow,
                     onupdate=datetime.datetime.utcnow)

    @classmethod
    def find_by_id(cls, _id):
        """Retrieve the record with the corresponding id from the database

        :param _id: ID of the record to be retrieved
        :return: Cls instance if record with the corresponding ID is found, otherwise None
        """

        return cls.query.get(_id)

    def update(self, **kwargs):
        """Update instance with keyword arguments or by unpacking a dict.

        :param kwargs:
        :return:
        """

        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self):
        """Commit changes of the current object to the database"""

        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Remove a record from the database"""

        db.session.delete(self)
        db.session.commit()

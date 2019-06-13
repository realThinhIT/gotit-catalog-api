
import datetime
from sqlalchemy import Column, Integer, DateTime
from main.database import db


class BaseModel(db.Model):
    """
    Provides common functionalities for model
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime,
                        default=datetime.datetime.utcnow,
                        onupdate=datetime.datetime.utcnow)

    @classmethod
    def find_by_id(cls, _id):
        """
        Retrieve the record with the corresponding id from the database

        :param _id: ID of the record to be retrieved
        :return: Cls instance if record with the corresponding ID is found, otherwise None
        """

        return cls.query.get(_id).one_or_none()

    def save(self):
        """
        Commit changes of the current object to the database
        """

        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Remove a record from the database
        """

        db.session.remove(self)
        db.session.commit()

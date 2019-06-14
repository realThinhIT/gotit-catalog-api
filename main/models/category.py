from sqlalchemy import Column, String
from main.models.base import BaseModel


class CategoryModel(BaseModel):
    __tablename__ = 'category'

    name = Column(String(64), nullable=False, unique=True)
    description = Column(String(255))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    @classmethod
    def get_all(cls):
        """
        Get all records of categories from the database.

        :return: A list of Category existing in the database
        """

        return cls.query.all()

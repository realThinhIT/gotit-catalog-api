from sqlalchemy import Column, String, Integer, ForeignKey
from main.models.base import BaseModel
from main.database import db


class ItemModel(BaseModel):
    """Model for Item"""

    __tablename__ = 'item'

    name = Column(String(64), nullable=False)
    description = Column(String(255))

    # Define foreign keys
    category_id = Column(Integer, ForeignKey('category.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    # Define relationships
    category = db.relationship('CategoryModel', back_populates='items', lazy=True)
    user = db.relationship('UserModel', back_populates='items', lazy=True)

    # Additional fields
    is_owner = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

        # If during object creation, description is null then init an empty string for it
        self.description = kwargs.get('description') if kwargs.get('description') is not None else ''

    @classmethod
    def get_with_pagination_by_category_id(cls, category_id, offset, limit):
        """Get records of a category with pagination.

        :return: A list of Category existing in the database with criteria
        """

        return cls.query.filter_by(category_id=category_id).offset(offset).limit(limit).all()

    @classmethod
    def count_items_by_category_id(cls, category_id):
        return cls.query.filter_by(category_id=category_id).count()

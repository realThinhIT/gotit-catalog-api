from marshmallow import Schema, fields, post_dump


class BaseSchema(Schema):
    """
    Base Schema for others
    """

    SKIP_VALUES = set([None])

    id = fields.Integer()
    updated = fields.DateTime()
    created = fields.DateTime()

    @post_dump
    def remove_skip_values(self, data):
        return {
            key: value for key, value in data.items()
            if value not in self.SKIP_VALUES
            or key in ['description']
        }

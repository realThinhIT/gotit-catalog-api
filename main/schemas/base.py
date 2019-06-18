from marshmallow import Schema, fields, post_dump


class BaseSchema(Schema):
    """Base Schema for other Schemas."""

    SKIP_VALUES = {None}

    id = fields.Integer()
    updated = fields.DateTime()
    created = fields.DateTime()

    @post_dump
    def remove_skip_values(self, data):
        """Remove skip values from the payload if it's being skipped and have None value.
        Mainly for is_owner field.
        """

        return {
            key: value for key, value in data.items()
            if value not in self.SKIP_VALUES
            or key in ['description']
        }

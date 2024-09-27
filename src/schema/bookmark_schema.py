from marshmallow import Schema, fields


class BookmarkSchema(Schema):
    id = fields.Int(required=True)
    body = fields.Str(required=True)
    url = fields.Str(required=True)
    short_url = fields.Str(allow_none=True)
    visits = fields.Int(allow_none=True)
    user_id = fields.Int(allow_none=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

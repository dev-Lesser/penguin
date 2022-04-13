"""
user favorite 사용하는 스키마
"""
from marshmallow import Schema, fields

class UserFavoriteScheme(Schema):
    id              = fields.Email(required=True)
    statId          = fields.String(required=True)
"""
Firebase 를 이용할 때 쓰는 스키마
"""
from marshmallow import Schema, fields, validate

class FirebaseMessageScheme(Schema):
    token   = fields.Str(required=True, validate=validate.Length(min=1))
    name    = fields.Str(required=True, validate=validate.Length(min=1))
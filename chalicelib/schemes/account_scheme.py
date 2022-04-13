"""
login 시에 사용하는 스키마
"""

from marshmallow import Schema, fields

class UserInfoScheme(Schema):
    id          = fields.Email(required=True)
    kind        = fields.Str(required=True)
    token       = fields.Str(required=True)
    fmtoken     = fields.Str(required=False)

class GetUserInfoScheme(Schema):
    id      = fields.Email(required=True)
    kind    = fields.Str(required=True)
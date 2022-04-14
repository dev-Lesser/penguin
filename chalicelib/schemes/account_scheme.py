"""
login 시에 사용하는 스키마
"""

from marshmallow import Schema, fields

class UserInfoScheme(Schema):
    id          = fields.Email(required=True)
    kind        = fields.String(required=True)
    token       = fields.String(required=True)
    fmtoken     = fields.String(required=False)

class GetUserInfoScheme(Schema):
    id      = fields.Email(required=True)
    kind    = fields.String(required=True)
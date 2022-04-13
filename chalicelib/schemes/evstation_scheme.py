"""
evstation 검색할 때 쓰는 스키마
"""
from marshmallow import Schema, fields, validate

class EvRecommendScheme(Schema):
    route = fields.List(
        fields.List(
            fields.Float(), 
            required=True, 
            validate=validate.Length(equal=2) # field 안 lat lng 의 pair
        ), 
        required=True, 
        validate=validate.Length(min=1)) # 최소 위경도 pair 1개
    distance = fields.Float(required=False)


class EvSearchScheme(Schema):
    maxx        = fields.Float(required=True)
    maxy        = fields.Float(required=True)
    minx        = fields.Float(required=True)
    miny        = fields.Float(required=True)
    currentXY   = fields.List(fields.Float(), required=False, validate=validate.Length(equal=2) )
    chgerType   = fields.String(required=False,     validate=validate.Length(equal=2)) # 충전기타입 01~07
    stat        = fields.String(required=False,     validate=validate.ContainsOnly(choices=['1','2','3','4','5','9'])) # 충전기상태 1~9
    output      = fields.Integer(required=False,    validate=validate.Range(min=3, max=200) ) # 충전 용량
    method      = fields.String(required=False,     validate=validate.Length(equal=2))  # 충전방식 단독/동시
    zcode       = fields.String(required=False,     validate=validate.Length(equal=2)) # 법정 코드
    parkingFree = fields.String(required=False,     validate=validate.ContainsOnly(choices=['Y','N']))
    bnm         = fields.String(required=False)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
